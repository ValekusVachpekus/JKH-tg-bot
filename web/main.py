import os
import sqlite3
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

load_dotenv()

DB_PATH = os.getenv("DB_PATH", "data/complaints.db")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")
SECRET_KEY = os.getenv("SECRET_KEY", "change-me-in-production")
MEDIA_DIR = Path("data/media")

app = FastAPI(title="ЖКХ Админ-панель")

templates = Jinja2Templates(directory="web/templates")
app.mount("/static", StaticFiles(directory="web/static"), name="static")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def check_auth(request: Request) -> bool:
    token = request.cookies.get("auth_token")
    return token == SECRET_KEY


def require_auth(request: Request):
    if not check_auth(request):
        raise HTTPException(status_code=302, headers={"Location": "/login"})
    return True


# ---------------------------------------------------------------------------
# Auth
# ---------------------------------------------------------------------------

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request, error: str = None):
    if check_auth(request):
        return RedirectResponse(url="/", status_code=302)
    return templates.TemplateResponse("login.html", {"request": request, "error": error})


@app.post("/login")
async def login(request: Request):
    form = await request.form()
    password = form.get("password", "")
    if password == ADMIN_PASSWORD:
        response = RedirectResponse(url="/", status_code=302)
        response.set_cookie("auth_token", SECRET_KEY, httponly=True, max_age=86400 * 7)
        return response
    return RedirectResponse(url="/login?error=1", status_code=302)


@app.get("/logout")
async def logout():
    response = RedirectResponse(url="/login", status_code=302)
    response.delete_cookie("auth_token")
    return response


# ---------------------------------------------------------------------------
# Dashboard
# ---------------------------------------------------------------------------

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    if not check_auth(request):
        return RedirectResponse(url="/login", status_code=302)
    
    db = get_db()
    
    # Stats
    total = db.execute("SELECT COUNT(*) FROM complaints").fetchone()[0]
    pending = db.execute("SELECT COUNT(*) FROM complaints WHERE status='pending'").fetchone()[0]
    accepted = db.execute("SELECT COUNT(*) FROM complaints WHERE status='accepted'").fetchone()[0]
    rejected = db.execute("SELECT COUNT(*) FROM complaints WHERE status='rejected'").fetchone()[0]
    blocked_count = db.execute("SELECT COUNT(*) FROM blocked_users").fetchone()[0]
    employees_count = db.execute("SELECT COUNT(*) FROM employees WHERE registered=1").fetchone()[0]
    
    # Recent complaints
    recent = db.execute("""
        SELECT id, fio, address, description, status, created_at 
        FROM complaints ORDER BY created_at DESC LIMIT 5
    """).fetchall()
    
    db.close()
    
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "stats": {
            "total": total,
            "pending": pending,
            "accepted": accepted,
            "rejected": rejected,
            "blocked": blocked_count,
            "employees": employees_count,
        },
        "recent_complaints": recent,
    })


# ---------------------------------------------------------------------------
# Complaints
# ---------------------------------------------------------------------------

@app.get("/complaints", response_class=HTMLResponse)
async def complaints_list(
    request: Request,
    status: str = None,
    search: str = None,
    page: int = 1,
):
    if not check_auth(request):
        return RedirectResponse(url="/login", status_code=302)
    
    db = get_db()
    per_page = 20
    offset = (page - 1) * per_page
    
    query = "SELECT * FROM complaints WHERE 1=1"
    params = []
    
    if status:
        query += " AND status = ?"
        params.append(status)
    
    if search:
        query += " AND (fio LIKE ? OR address LIKE ? OR description LIKE ?)"
        search_param = f"%{search}%"
        params.extend([search_param, search_param, search_param])
    
    # Count total
    count_query = query.replace("SELECT *", "SELECT COUNT(*)")
    total = db.execute(count_query, params).fetchone()[0]
    
    # Get page
    query += " ORDER BY created_at DESC LIMIT ? OFFSET ?"
    params.extend([per_page, offset])
    complaints = db.execute(query, params).fetchall()
    
    db.close()
    
    total_pages = (total + per_page - 1) // per_page
    
    return templates.TemplateResponse("complaints.html", {
        "request": request,
        "complaints": complaints,
        "current_status": status,
        "search": search or "",
        "page": page,
        "total_pages": total_pages,
        "total": total,
    })


@app.get("/complaints/{complaint_id}", response_class=HTMLResponse)
async def complaint_detail(request: Request, complaint_id: int):
    if not check_auth(request):
        return RedirectResponse(url="/login", status_code=302)
    
    db = get_db()
    complaint = db.execute("SELECT * FROM complaints WHERE id = ?", (complaint_id,)).fetchone()
    
    if not complaint:
        db.close()
        raise HTTPException(status_code=404, detail="Жалоба не найдена")
    
    # Get employee who accepted/rejected
    accepted_by_info = None
    if complaint["accepted_by"]:
        accepted_by_info = db.execute(
            "SELECT fio, position FROM employees WHERE user_id = ?",
            (complaint["accepted_by"],)
        ).fetchone()
    
    db.close()
    
    return templates.TemplateResponse("complaint_detail.html", {
        "request": request,
        "complaint": complaint,
        "accepted_by_info": accepted_by_info,
    })


@app.post("/complaints/{complaint_id}/accept")
async def accept_complaint(request: Request, complaint_id: int):
    if not check_auth(request):
        return RedirectResponse(url="/login", status_code=302)
    
    db = get_db()
    db.execute(
        "UPDATE complaints SET status = 'accepted' WHERE id = ? AND status = 'pending'",
        (complaint_id,)
    )
    db.commit()
    db.close()
    return RedirectResponse(url=f"/complaints/{complaint_id}", status_code=302)


@app.post("/complaints/{complaint_id}/reject")
async def reject_complaint(request: Request, complaint_id: int):
    if not check_auth(request):
        return RedirectResponse(url="/login", status_code=302)
    
    db = get_db()
    db.execute(
        "UPDATE complaints SET status = 'rejected' WHERE id = ? AND status = 'pending'",
        (complaint_id,)
    )
    db.commit()
    db.close()
    return RedirectResponse(url=f"/complaints/{complaint_id}", status_code=302)


# ---------------------------------------------------------------------------
# Employees
# ---------------------------------------------------------------------------

@app.get("/employees", response_class=HTMLResponse)
async def employees_list(request: Request):
    if not check_auth(request):
        return RedirectResponse(url="/login", status_code=302)
    
    db = get_db()
    employees = db.execute("""
        SELECT * FROM employees ORDER BY registered DESC, added_at DESC
    """).fetchall()
    db.close()
    
    return templates.TemplateResponse("employees.html", {
        "request": request,
        "employees": employees,
    })


@app.post("/employees/add")
async def add_employee(request: Request):
    if not check_auth(request):
        return RedirectResponse(url="/login", status_code=302)
    
    form = await request.form()
    username = form.get("username", "").lstrip("@").lower().strip()
    
    if not username:
        return RedirectResponse(url="/employees?error=empty", status_code=302)
    
    db = get_db()
    existing = db.execute("SELECT 1 FROM employees WHERE username = ?", (username,)).fetchone()
    if existing:
        db.close()
        return RedirectResponse(url="/employees?error=exists", status_code=302)
    
    db.execute("INSERT INTO employees (username) VALUES (?)", (username,))
    db.commit()
    db.close()
    return RedirectResponse(url="/employees?success=1", status_code=302)


@app.post("/employees/delete/{username}")
async def delete_employee(request: Request, username: str):
    if not check_auth(request):
        return RedirectResponse(url="/login", status_code=302)
    
    db = get_db()
    db.execute("DELETE FROM employees WHERE username = ?", (username,))
    db.commit()
    db.close()
    return RedirectResponse(url="/employees", status_code=302)


# ---------------------------------------------------------------------------
# Media serving
# ---------------------------------------------------------------------------

@app.get("/media/{filename}")
async def serve_media(request: Request, filename: str):
    if not check_auth(request):
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    file_path = MEDIA_DIR / filename
    if not file_path.exists() or not file_path.is_file():
        raise HTTPException(status_code=404, detail="File not found")
    
    # Security: prevent directory traversal
    if not str(file_path.resolve()).startswith(str(MEDIA_DIR.resolve())):
        raise HTTPException(status_code=403, detail="Access denied")
    
    return FileResponse(file_path)


# ---------------------------------------------------------------------------
# Blocked users
# ---------------------------------------------------------------------------

@app.get("/blocked", response_class=HTMLResponse)
async def blocked_list(request: Request):
    if not check_auth(request):
        return RedirectResponse(url="/login", status_code=302)
    
    db = get_db()
    blocked = db.execute("SELECT * FROM blocked_users ORDER BY blocked_at DESC").fetchall()
    db.close()
    
    return templates.TemplateResponse("blocked.html", {
        "request": request,
        "blocked_users": blocked,
    })


@app.post("/blocked/unblock/{user_id}")
async def unblock_user(request: Request, user_id: int):
    if not check_auth(request):
        return RedirectResponse(url="/login", status_code=302)
    
    db = get_db()
    db.execute("DELETE FROM blocked_users WHERE user_id = ?", (user_id,))
    db.commit()
    db.close()
    return RedirectResponse(url="/blocked", status_code=302)


# ---------------------------------------------------------------------------
# API endpoints (for potential future use)
# ---------------------------------------------------------------------------

@app.get("/api/stats")
async def api_stats(request: Request):
    if not check_auth(request):
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    db = get_db()
    stats = {
        "total": db.execute("SELECT COUNT(*) FROM complaints").fetchone()[0],
        "pending": db.execute("SELECT COUNT(*) FROM complaints WHERE status='pending'").fetchone()[0],
        "accepted": db.execute("SELECT COUNT(*) FROM complaints WHERE status='accepted'").fetchone()[0],
        "rejected": db.execute("SELECT COUNT(*) FROM complaints WHERE status='rejected'").fetchone()[0],
    }
    db.close()
    return stats


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
