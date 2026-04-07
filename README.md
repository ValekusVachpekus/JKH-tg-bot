# 🏠 Housing Utilities Assistant - Telegram Bot + Web Panel

A complaint management system for housing maintenance requests.

## Demo

### Screenshots

**Admin Web Panel:**
<img width="3070" height="1516" alt="image" src="https://github.com/user-attachments/assets/89dc83b0-a245-4dc4-ae1c-75a307db782c" />
<img width="3070" height="1508" alt="image" src="https://github.com/user-attachments/assets/f37d3514-9aa9-4cf8-964c-6c0cb81799e4" />
<img width="3070" height="1514" alt="image" src="https://github.com/user-attachments/assets/d10b1942-05de-4a7e-ba05-eb591401b452" />
<img width="3070" height="1514" alt="image" src="https://github.com/user-attachments/assets/b8629919-9604-4cbf-a430-851af02d1dbb" />
<img width="3070" height="1514" alt="image" src="https://github.com/user-attachments/assets/c8ff9244-0523-4686-a008-03e9c4fd9baf" />

**Employee Web Panel:**
<img width="3070" height="1510" alt="image" src="https://github.com/user-attachments/assets/d392ccb1-78c9-455d-a89f-0be2e716c1c9" />


**Telegram Bot - Complaint Submission:**
<img width="1258" height="1496" alt="image" src="https://github.com/user-attachments/assets/d7cd1358-f7be-4d32-85d9-afcbf3b27ebf" />
<img width="762" height="342" alt="image" src="https://github.com/user-attachments/assets/7ca50cf1-21d8-4369-b213-494ba3355e40" />
<img width="822" height="560" alt="image" src="https://github.com/user-attachments/assets/689190d4-4cca-4592-a173-75d7029569e7" />


**User Web Panel:**
<img width="2116" height="1512" alt="image" src="https://github.com/user-attachments/assets/692828b4-a212-4499-b3bd-073babc85ea0" />

## Product Context

### End Users
- **Residents** - submit complaints about housing issues
- **Employees** - maintenance workers who handle complaints
- **Admin** - manages employees and oversees the system

### Problem
Residents struggle with slow feedback and lost requests in messenger groups. Staff lack a centralized tool to track ticket history and manage maintenance tasks.

### Solution
A unified ecosystem for seamless submission, tracking, and management of housing maintenance requests through Telegram bot and web interface.

## Features

### Telegram Bot
- **Residents** - submit complaints (full name, address, issue description, photo/video)
- **Employees** - accept/reject complaints
- **Administrator** - manage employees, handle complaints
- **Rating System** - residents rate work quality (1-5 ⭐)
- User blocking
- Status notifications with employee information
- Archiving processed complaints to archive group

### Admin Web Panel
- 📊 **Dashboard** - statistics, charts (Chart.js)
- 📋 **Complaints** - list with filters, search, pagination, accept/reject with notifications
- 👷 **Employees** - add/remove staff members
- ⭐ **Ratings** - employee statistics, reviews
- 🚫 **Blocked Users** - manage blocked users

### Employee Web Panel
- 📋 **Complaints** - list with filters, search, pagination, accept/reject complaints
- ⭐ **Ratings** - employee statistics, reviews
- 🔗 **Login** - one-time code from Telegram (`/link_account`)

### User Web Panel (Residents)
- 📋 **My Complaints** - list of all complaints with statuses and ratings
- 📝 **Submit Complaint** - form (full name, address, description, photo/video upload or link)
- 📄 **Complaint Details** - view status, employee info, rejection reason
- ⭐ **Rate Work** - rate completed work quality (1-5 stars + review)
- 🔗 **Login** - one-time code from Telegram (`/link_account`)

## Tech Stack

- **Bot**: Python 3.12, aiogram 3.15
- **Web**: FastAPI, Jinja2, Tailwind CSS, Chart.js
- **Database**: SQLite (aiosqlite)
- **Deployment**: Docker Compose
- **Notifications**: aiohttp (Telegram Bot API)

## Project Structure

```
Toolkit-tg-bot/
├── bot/
│   ├── main.py              # Bot entry point
│   ├── config.py            # Configuration (env)
│   ├── database.py          # Database initialization, migrations
│   ├── states.py            # FSM states
│   ├── keyboards.py         # Inline keyboards
│   ├── media_utils.py       # Media download utilities
│   ├── logging_config.py    # Logging setup
│   └── handlers/
│       ├── user.py          # User commands (/complaint, /rate)
│       ├── employee.py      # Employee commands (/register, /link_account)
│       └── admin.py         # Admin commands (/add_employee, /staff)
├── web/
│   ├── main.py              # FastAPI application
│   ├── auth.py              # Authentication (admin/employee)
│   ├── config.py            # Web panel configuration
│   ├── database.py          # SQLite connection
│   ├── logging_config.py    # Logging
│   ├── static/              # CSS styles
│   └── templates/
│       ├── base.html        # Base template
│       ├── login.html       # Login page
│       ├── admin/           # Admin templates
│       │   ├── dashboard.html
│       │   ├── complaints.html
│       │   ├── complaint_detail.html
│       │   ├── employees.html
│       │   ├── ratings.html
│       │   └── blocked.html
│       └── employee/        # Employee templates
│           ├── complaints.html
│           ├── complaint_detail.html
│           └── ratings.html
│       └── user/            # User templates
│           ├── complaints.html
│           ├── complaint_form.html
│           ├── complaint_detail.html
│           └── rate.html
├── data/                    # Database + media (auto-created)
├── logs/                    # Logs (auto-created)
├── docker-compose.yml
├── Dockerfile.bot
├── Dockerfile.web
├── requirements.txt
└── .env.example
```

## Database Schema

SQLite database with tables:
- `complaints` — complaints (id, user_id, fio, address, description, media, status, rating, review, rejection_reason...)
- `employees` — employees (user_id, username, fio, position, area, registered, web_linked)
- `blocked_users` — blocked users
- `complaint_messages` — message IDs for button invalidation
- `verification_codes` — codes for web panel account linking

## Usage

### 1. Manual Setup (Version 1 - Direct Run)
1. Install Python 3.12: `sudo apt install python3.12`
2. Create virtual environment: `python3 -m venv venv && source venv/bin/activate`
3. Install dependencies: `pip install -r requirements.txt`
4. Configure environment: `cp .env.example .env`, `nano .env`
5. Run: `python -m bot.main` (bot) and `uvicorn web.main:app` (web)

### 2. Docker (Version 2 - Recommended)

#### Requirements

- **OS**: Ubuntu 24.04 (or compatible Linux system)
- **Docker**: 24.0 or newer
- **Docker Compose**: v2.0 or newer

#### 1. Configure environment variables
```bash
cp .env.example .env
```

Edit `.env`:
```env
BOT_TOKEN=your_bot_token          # Token from @BotFather
ADMIN_ID=123456789                # Your Telegram ID
LOG_CHAT_ID=-100123456789         # Archive group ID (optional)
ADMIN_PASSWORD=secure_password    # Admin password for web panel
SECRET_KEY=random_secret_key      # Secret key for sessions
DB_PATH=data/complaints.db        # Database path
```

**How to get BOT_TOKEN:** [@BotFather](https://t.me/BotFather) → `/newbot`

**How to get ADMIN_ID:** [@userinfobot](https://t.me/userinfobot)

**How to get LOG_CHAT_ID:** Create a group, add bot, send a message and check via API

#### 2. Start with Docker
```bash
docker compose up -d --build
```

**Access**
- Telegram bot: send `/start` to your bot
- Admin web panel: http://localhost:8000 (password from `ADMIN_PASSWORD`)
- Employee web panel: http://localhost:8000 (code from `/link_account` in bot)
- User web panel: http://localhost:8000 (code from `/link_account` in bot)

Complaints submitted via web panel are automatically sent to employees in Telegram with action buttons.

#### Stop
```bash
docker compose down
```

## Deployment

### Deployment on VM

#### System Requirements

- **OS**: Ubuntu 24.04 LTS
- **Software**:
  - Docker Engine 24.0+
  - Docker Compose v2+
  - Git

#### Step-by-Step Instructions

1. **Install Docker and Docker Compose** (if not installed):
   ```bash
   # Update packages
   sudo apt update
   
   # Install Docker
   sudo apt install -y docker.io docker-compose-v2
   
   # Add user to docker group
   sudo usermod -aG docker $USER
   newgrp docker
   ```

2. **Clone repository**:
   ```bash
   git clone https://github.com/ValekusVachpekus/se-toolkit-hackathon.git
   cd se-toolkit-hackathon
   ```

3. **Configure environment variables**:
   ```bash
   cp .env.example .env
   nano .env  # or use any text editor
   ```
   
   Required fields:
   - `BOT_TOKEN` - token from @BotFather
   - `ADMIN_ID` - your Telegram ID
   - `ADMIN_PASSWORD` - password for web panel
   - `SECRET_KEY` - random string for sessions
   - `LOG_CHAT_ID` - (optional) archive group ID

4. **Create required directories**:
   ```bash
   mkdir -p data logs
   chmod 777 data logs
   ```

5. **Start application**:
   ```bash
   docker compose up -d --build
   ```

6. **Check status**:
   ```bash
   docker compose ps
   docker compose logs -f
   ```

7. **Access application**:
   - Telegram bot: send `/start` to your bot
   - Web panel: `http://<VM_IP>:8000`

#### Update Application

```bash
cd se-toolkit-hackathon
git pull
docker compose down
docker compose up -d --build
```

#### Stop Application

```bash
docker compose down
```

#### Full Cleanup (including data)

```bash
docker compose down -v
rm -rf data logs
```

## Telegram Bot Commands

### For Residents
| Command | Description |
|---------|----------|
| `/start` | Start using the bot |
| `/complaint` | Submit a complaint (4 steps) |
| `/rate` | Rate completed work |
| `/link_account` | Get login code for web panel |

### For Employees
| Command | Description |
|---------|----------|
| `/register` | Register (after admin adds you) |
| `/complaints` | View active complaints |
| `/link_account` | Get login code for web panel |

### For Administrator
| Command | Description |
|---------|----------|
| `/add_employee` | Add employee by username |
| `/staff` | View employee list |
| `/complaints` | View active complaints |
| `/blocked` | View blocked users |

## Web Panel

### Login
- **Administrator**: password from `.env`
- **Employee**: one-time 6-digit code from `/link_account` command
- **User**: one-time 6-digit code from `/link_account` command

### Admin Panel (`/admin/*`)
- **Dashboard** - statistics cards + 3 charts (pie, bar, line)
- **Complaints** - filters by status, search, pagination
- **Complaint Details** - media view, accept/reject with reason
- **Employees** - add/remove staff
- **Ratings** - average employee ratings, recent reviews
- **Blocked Users** - list of blocked users with unblock option

### Employee Panel (`/employee/*`)
- **Complaints** - view, accept/reject complaints
- **Ratings** - overall statistics

### User Panel (`/user/*`)
- **My Complaints** (`/user/complaints`) - list of all complaints with statuses
- **Submit Complaint** (`/user/complaints/new`) - form with media upload
- **Complaint Details** (`/user/complaints/{id}`) - full info, status, assigned employee
- **Rate Work** (`/user/complaints/{id}/rate`) - rate 1-5 stars + review

## Implemented Features

- [x] Telegram bot with FSM
- [x] Complaint submission (full name, address, description, media)
- [x] Admin panel
- [x] Employee panel
- [x] User panel (residents)
- [x] Rating system (1-5 stars + review)
- [x] Dashboard charts
- [x] Notifications via Telegram API
- [x] Archiving to log group
- [x] Employee/user login with codes
- [x] Media upload to Telegram from web panel
- [x] Button invalidation after complaint processing
- [x] Public complaint submission form

## Future Improvements

- [ ] Export complaints to CSV/Excel
- [ ] PostgreSQL for production
- [ ] Push notifications in web panel

## License

[MIT License](LICENSE)

## Author

- **Name**: Shchetkov Ilia Alexeevich
- **GitHub**: [ValekusVachpekus](https://github.com/ValekusVachpekus)
- **Email**: i.shchetkov@innopolis.university

Created as part of the Software Engineering Toolkit course at Innopolis University

