from pathlib import Path
from tempfile import TemporaryDirectory

from aiogram import Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import FSInputFile, Message

from download_bot.services.downloader import YouTubeDownloader
from download_bot.services.parser import extract_youtube_url


router = Router()
downloader = YouTubeDownloader()


def _is_too_large_error(error: Exception) -> bool:
    text = str(error).lower()
    return (
        "request entity too large" in text
        or "file is too big" in text
        or "size exceeds" in text
    )


@router.message()
async def youtube_handler(message: Message) -> None:
    if not message.text:
        return

    url = extract_youtube_url(message.text)

    if url is None:
        return

    status_message = await message.reply("📥 Скачиваю...")

    try:
        for max_height in (720, 480, 360, 240):
            try:
                with TemporaryDirectory() as temp_dir:
                    path = await downloader.download(
                        url,
                        Path(temp_dir),
                        max_height=max_height,
                    )

                    await message.reply_video(
                        video=FSInputFile(path),
                    )

                await status_message.delete()
                return
            except TelegramBadRequest as error:
                if not _is_too_large_error(error):
                    raise

                continue
            except Exception as error:
                if _is_too_large_error(error):
                    continue
                raise

        await status_message.edit_text(
            "❌ Видео слишком большое для Telegram. Попробуйте ссылку на более короткое или менее тяжёлое видео."
        )

    except Exception as error:
        await status_message.edit_text(
            f"❌ Ошибка:\n<code>{error}</code>"
        )