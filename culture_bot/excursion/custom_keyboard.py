from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from .models import Route

routs = Route.objects.all()

button_ways = [
    *[[InlineKeyboardButton(text=rout.title)] for rout in routs],
    [InlineKeyboardButton(text='О проекте')],
    [InlineKeyboardButton(text='Что ты умеешь?')],
]

keyboard_ways = InlineKeyboardMarkup(inline_keyboard=button_ways)
# keyboard_ways.add(*button_ways)
def get_keyboard():
    # Генерация клавиатуры.
    buttons = [
        InlineKeyboardButton(text="-1", callback_data="num_decr"),
        InlineKeyboardButton(text="+1", callback_data="num_incr"),
        InlineKeyboardButton(text="Подтвердить", callback_data="num_finish")
    ]
    # Благодаря row_width=2, в первом ряду будет две кнопки, а оставшаяся одна
    # уйдёт на следующую строку
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    return keyboard

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
