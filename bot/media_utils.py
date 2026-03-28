import asyncio
from pathlib import Path

from aiogram import Bot

from bot.config import MEDIA_DIR, logger


async def download_media(bot: Bot, media_file_id: str, media_type: str, user_id: int) -> str | None:
    """
    Download media file from Telegram to local storage.
    
    Returns: local file path if successful, None otherwise
    """
    try:
        file = await bot.get_file(media_file_id)
        extension = {
            "photo": "jpg",
            "video": "mp4",
            "document": file.file_path.split(".")[-1] if "." in file.file_path else "bin"
        }.get(media_type, "bin")
        
        filename = f"{user_id}_{int(asyncio.get_event_loop().time())}_{media_file_id[:10]}.{extension}"
        local_path = MEDIA_DIR / filename
        
        await bot.download_file(file.file_path, local_path)
        logger.info(f"Downloaded media: {local_path}")
        return str(local_path)
    except Exception as e:
        logger.error(f"Failed to download media: {e}")
        return None
