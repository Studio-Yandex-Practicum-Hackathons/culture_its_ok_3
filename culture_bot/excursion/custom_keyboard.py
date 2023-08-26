from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from .models import Route

routs = Route.objects.all()

button_ways = [
    *[[KeyboardButton(text=f'/map {rout.title}')] for rout in routs],
    [KeyboardButton(text='О проекте')],
    [KeyboardButton(text='Что ты умеешь?')],
]

keyboard_ways = ReplyKeyboardMarkup(keyboard=button_ways)
# keyboard_ways.add(*button_ways)


keyboard_yes_no = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Да'), ],
        [KeyboardButton(text='Нет'), ],
    ],
    resize_keyboard=True,
)

keyboard_go_on_or_stop = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Идём дальше!'), ],
        [KeyboardButton(text='Завершить маршрут'), ],
    ],
    resize_keyboard=True,
)

keyboard_yes_or_stop = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Да'), ],
        [KeyboardButton(text='Завершить маршрут'), ],
    ],
    resize_keyboard=True,
)

keyboard_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Меню'), ],
    ],
    resize_keyboard=True,
)
