import sys
import logging
from aiogram import Bot, Dispatcher, html
from aiohttp import ClientSession
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
import asyncio
from handlers import router as h_router
from config import Config
from depends import init_session, close_session, init_service

dp = Dispatcher()


@dp.startup()
async def on_startup():
    await init_session()
    await init_service()


@dp.shutdown()
async def on_shutdown():
    await close_session()
    

async def main():
    
    bot = Bot(token=Config.TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp.include_router(h_router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

    
    
