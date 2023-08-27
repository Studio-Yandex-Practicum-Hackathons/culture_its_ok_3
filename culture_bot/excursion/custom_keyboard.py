from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           KeyboardButton, ReplyKeyboardMarkup)

from .models import Route

routs = Route.objects.all()

button_ways = [
    *[[KeyboardButton(text=f'/map {rout.title}')] for rout in routs],
    [KeyboardButton(text='О проекте')],
    [KeyboardButton(text='Что ты умеешь?')],
]

keyboard_ways = ReplyKeyboardMarkup(
    keyboard=button_ways,
    resize_keyboard=True,
    one_time_keyboard=True
)

keyboard_yes_no = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='/yes'), ],
        [KeyboardButton(text='/no'), ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

keyboard_go_on_or_stop = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='/next'), ],
        [KeyboardButton(text='/end'), ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

keyboard_yes_or_stop = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='/yes'), ],
        [KeyboardButton(text='/end'), ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

keyboard_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Меню'), ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

keyboard_rating = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='1',), KeyboardButton(text='2',),
         KeyboardButton(text='3',), KeyboardButton(text='4',),
         KeyboardButton(text='5',)
         ],
        [KeyboardButton(text='6',), KeyboardButton(text='7',),
         KeyboardButton(text='8',), KeyboardButton(text='9',),
         KeyboardButton(text='10',)
         ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)
