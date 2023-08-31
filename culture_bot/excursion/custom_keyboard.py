from random import randint

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from .messages import *
from .models import Route

routs = Route.objects.all()


def keyboard_ways():
    button_ways = [[KeyboardButton(text=rout.title)] for rout in routs if rout.show]

    return ReplyKeyboardMarkup(
        keyboard=[
            *button_ways,
            [KeyboardButton(text='О проекте')],
            [KeyboardButton(text='Что ты умеешь?')],
        ],
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


def keyboard_go_on_or_stop():
    but = LET_MOVE_ON[randint(0, len(LET_MOVE_ON)-1)]
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=but, )],
            [KeyboardButton(text='Завершить медитацию'), ],
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


def keyboard_ready():
    but = SEARCH_FOR_PLACE[randint(0, len(SEARCH_FOR_PLACE)-1)]
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='Я готов',), ],
            [KeyboardButton(text=but)]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )


keyboard_only_ready = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Я готов',), ],
        [KeyboardButton(text='Завершить медитацию')]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)
