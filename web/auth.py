from fastapi import HTTPException, Request

from web.config import SECRET_KEY


def check_auth(request: Request) -> bool:
    token = request.cookies.get("auth_token")
    return token == SECRET_KEY


def require_auth(request: Request):
    if not check_auth(request):
        raise HTTPException(status_code=302, headers={"Location": "/login"})
    return True
