from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

keyboard_ways = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(
            text='Маршрут 1. "Руки бы им оторвать"'
        ), ],
        [KeyboardButton(
            text='Маршрут 2. "Не с кем играть. Играю со стенкой"'
        ), ],
        [KeyboardButton(
            text='Маршрут 3. "… но спи/СМИ спокойно"'
        ), ],
        [KeyboardButton(text='О проекте'), ],
        [KeyboardButton(text='Что ты умеешь?'), ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

keyboard_yes_no = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Да'), ],
        [KeyboardButton(text='Нет'), ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

keyboard_go_on_or_stop = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Идём дальше!'), ],
        [KeyboardButton(text='Завершить маршрут'), ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

keyboard_yes_or_stop = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Да'), ],
        [KeyboardButton(text='Завершить маршрут'), ],
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