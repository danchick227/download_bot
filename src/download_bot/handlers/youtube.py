from pathlib import Path
from tempfile import TemporaryDirectory

from aiogram import Router
from aiogram.types import FSInputFile, Message

from download_bot.services.downloader import YouTubeDownloader
from download_bot.services.parser import extract_youtube_url


router = Router()
downloader = YouTubeDownloader()


@router.message()
async def youtube_handler(message: Message) -> None:
    if not message.text:
        return

    url = extract_youtube_url(message.text)

    if url is None:
        return

    status_message = await message.reply("📥 Скачиваю...")

    try:
        with TemporaryDirectory() as temp_dir:
            path = await downloader.download(
                url,
                Path(temp_dir),
            )

            await message.reply_video(
                video=FSInputFile(path),
            )

        await status_message.delete()

    except Exception as error:
        await status_message.edit_text(
            f"❌ Ошибка:\n<code>{error}</code>"
        )