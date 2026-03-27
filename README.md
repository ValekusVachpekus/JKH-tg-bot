# 🏠 ЖКХ Toolkit - Telegram Bot + Admin Panel

Система приёма жалоб от жителей на проблемы ЖКХ (жилищно-коммунального хозяйства).

## 🎯 Возможности

### Telegram Bot
- **Жители** подают жалобы (ФИО, адрес, суть проблемы, фото/видео)
- **Администратор** управляет работниками, обрабатывает жалобы
- **Работники** принимают/отклоняют жалобы
- Блокировка пользователей
- Уведомления о статусе жалобы

### Веб-панель администратора
- 📊 Дашборд со статистикой
- 📋 Список жалоб с фильтрами и поиском
- 👷 Управление работниками (добавление/удаление)
- 🚫 Управление заблокированными пользователями
- ✅/❌ Принятие/отклонение жалоб из браузера

## 🛠 Технологии

- **Backend**: Python 3.12 (aiogram 3.15, FastAPI)
- **Database**: SQLite
- **Web**: HTML + Tailwind CSS + Jinja2
- **Deploy**: Docker Compose

## 🚀 Быстрый старт

### 1. Клонировать репозиторий
```bash
git clone <repo-url>
cd Toolkit-tg-bot
```

### 2. Настроить переменные окружения
```bash
cp .env.example .env
```

Отредактировать `.env`:
```env
BOT_TOKEN=your_bot_token_here        # Токен от @BotFather
ADMIN_ID=123456789                   # Ваш Telegram ID
ADMIN_PASSWORD=your_secure_password  # Пароль для веб-панели
SECRET_KEY=random_secret_key         # Секретный ключ для сессий
```

**Как получить BOT_TOKEN:**
1. Напишите [@BotFather](https://t.me/BotFather)
2. Отправьте `/newbot`
3. Следуйте инструкциям
4. Скопируйте токен

**Как узнать свой ADMIN_ID:**
1. Напишите [@userinfobot](https://t.me/userinfobot)
2. Скопируйте Id

### 3. Запустить через Docker
```bash
docker-compose up -d
```

**Готово!** 
- Telegram бот работает (напишите ему `/start`)
- Веб-панель: http://localhost:8000 (логин: пароль из `ADMIN_PASSWORD`)

### Остановить
```bash
docker-compose down
```

## 📱 Использование

### Telegram Bot

**Для жителей:**
- `/start` — начало работы
- `/complaint` — подать жалобу

**Для администратора:**
- `/add_employee` — добавить работника
- `/staff` — список работников
- `/complaints` — активные жалобы
- `/blocked` — заблокированные пользователи

**Для работников:**
- `/register` — регистрация после добавления админом
- `/complaints` — активные жалобы

### Веб-панель

1. Откройте http://localhost:8000
2. Введите пароль из `.env`
3. Используйте:
   - **Дашборд** — общая статистика
   - **Жалобы** — просмотр, фильтрация, принятие/отклонение
   - **Работники** — добавление и удаление
   - **Заблокированные** — разблокировка пользователей

## 📁 Структура проекта

```
Toolkit-tg-bot/
├── bot.py                 # Telegram бот
├── web/
│   ├── main.py            # FastAPI приложение
│   ├── templates/         # HTML шаблоны
│   └── static/            # CSS стили
├── data/                  # База данных (создаётся автоматически)
├── requirements.txt       # Python зависимости
├── .env.example           # Пример конфигурации
├── Dockerfile.bot         # Docker образ для бота
├── Dockerfile.web         # Docker образ для веб-панели
└── docker-compose.yml     # Оркестрация сервисов
```

## 🗃 База данных

SQLite с таблицами:
- `complaints` — жалобы
- `employees` — работники
- `blocked_users` — заблокированные
- `complaint_messages` — сообщения для удаления кнопок

## 🔧 Разработка

### Локальный запуск без Docker

**Бот:**
```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python bot.py
```

**Веб-панель:**
```bash
python -m uvicorn web.main:app --reload --host 0.0.0.0 --port 8000
```

## 📝 TODO / Будущие улучшения

- [ ] Панель работника (упрощённый доступ)
- [ ] Публичная форма подачи жалоб (альтернатива Telegram)
- [ ] Уведомления работникам в Telegram при новой жалобе
- [ ] Статистика по работникам
- [ ] Экспорт жалоб в CSV/Excel
- [ ] PostgreSQL вместо SQLite (для production)

## 🐛 Troubleshooting

**Бот не отвечает:**
- Проверьте токен в `.env`
- Проверьте `docker-compose logs bot`

**Веб-панель не открывается:**
- Проверьте `docker-compose logs web`
- Убедитесь, что порт 8000 свободен

**Internal Server Error при логине:**
- Пересоберите контейнер: `docker-compose build web && docker-compose up -d web`

## 📄 Лицензия

MIT

## 👤 Автор

Создано для учебного проекта.
