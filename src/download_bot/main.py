from download_bot.config import BOT_TOKEN
from download_bot.handlers import router as main_router

import asyncio

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties


async def main() -> None:
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    await dp.start_polling(bot)


dp = Dispatcher()
dp.include_router(main_router)

if __name__ == '__main__':
    asyncio.run(main())