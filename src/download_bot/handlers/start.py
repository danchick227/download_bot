from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

router = Router()

@router.message(CommandStart())
async def start(message: Message) -> None:
    await message.answer(
        "Это бот для скачивания видео с ютуба.\n Отправь мне ссылку на видео"
    )