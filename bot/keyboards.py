from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def complaint_keyboard(complaint_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="✅ Принять",       callback_data=f"accept_{complaint_id}"),
        InlineKeyboardButton(text="❌ Отклонить",     callback_data=f"reject_{complaint_id}"),
        InlineKeyboardButton(text="🚫 Заблокировать", callback_data=f"block_{complaint_id}"),
    ]])


def build_complaint_text(complaint_id, uname, user_id, fio, address, description) -> str:
    return (
        f"📨 <b>Новая жалоба #{complaint_id}</b>\n\n"
        f"👤 <b>От:</b> {uname} (ID: <code>{user_id}</code>)\n"
        f"📋 <b>ФИО заявителя:</b> {fio}\n"
        f"🏠 <b>Адрес:</b> {address}\n"
        f"📝 <b>Суть жалобы:</b> {description}"
    )
