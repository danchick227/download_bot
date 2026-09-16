from aiogram import Router

from .start import router as start_router
from .youtube import router as youtube_router

router = Router()

router.include_routers(start_router, youtube_router)
