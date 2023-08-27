import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from django.core.management.base import BaseCommand
from dotenv import load_dotenv

from excursion.handlers import router
from excursion.models import *

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
# TELEGRAM_TOKEN = '5575568139:AAEuNC2x_yW23LFcefoBmmsc7AZw31abqyA'
# TELEGRAM_CHAT_ID = '350114238'


async def main():
    bot = Bot(token=TELEGRAM_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


class Command(BaseCommand):
    help = 'Телеграм-бот'

    def handle(self, *args, **options):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s, %(levelname)s, %(message)s',
        )
        asyncio.run(main())
