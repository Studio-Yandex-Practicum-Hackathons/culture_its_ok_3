from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage


TOKEN_API = '6560049240:AAGI8IQSekgA2BvhavLWJ9o6MUvHoAtLA7I'

storage = MemoryStorage()

bot = Bot(TOKEN_API)
dp = Dispatcher(bot, storage=storage)
