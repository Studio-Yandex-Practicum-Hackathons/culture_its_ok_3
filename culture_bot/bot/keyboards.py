from aiogram import types


# Клавиатура выбора маршрута
routes_button_1 = types.InlineKeyboardButton(text="Маршрут 1")
routes_button_2 = types.InlineKeyboardButton(text="Маршрут 2")
routes_button_3 = types.InlineKeyboardButton(text="Маршрут 3")
routes_keyboard = types.ReplyKeyboardMarkup(
    resize_keyboard=True,
    input_field_placeholder="Выберите способ",
    one_time_keyboard=True
)
routes_keyboard.add(routes_button_1).add(routes_button_2).add(routes_button_3)

# Клавиатура выхода из маршрута
exit_button_1 = types.KeyboardButton(text="Возобновить прохождение маршрута")
exit_button_2 = types.KeyboardButton(text="Покинуть маршрут")
exit_keyboard = types.ReplyKeyboardMarkup(
    resize_keyboard=True,
    input_field_placeholder="Выберите способ",
    one_time_keyboard=True
)
exit_keyboard.add(exit_button_1).add(exit_button_2)

# Подтверждение готовности к прохождению маршрута
ready_kb = [
    [
        types.KeyboardButton(text="Начнем"),
    ],
    [
        types.KeyboardButton(text="Нет, не готов")
    ]
]
ready_keyboard = types.ReplyKeyboardMarkup(
    keyboard=ready_kb,
    resize_keyboard=True,
    input_field_placeholder="Выберите способ",
    one_time_keyboard=True
)

# Подтверждение местоположения
location_kb = [
    [
        types.KeyboardButton(text="Да")
    ],
    [
        types.KeyboardButton(text="Нет")
    ]
]
location_keyboard = types.ReplyKeyboardMarkup(
    keyboard=location_kb,
    resize_keyboard=True,
    input_field_placeholder="Находитесь вы в этом месте?",
    one_time_keyboard=True
)

# Повторное подтверждение местоположения
location_kb2 = [
    [
        types.KeyboardButton(text="Я на месте."),
    ],
]
location_keyboard2 = types.ReplyKeyboardMarkup(
    keyboard=location_kb2,
    resize_keyboard=True,
    input_field_placeholder="Выберите способ",
    one_time_keyboard=True
)

# Следующая достопримечательность
next_keyboard = types.ReplyKeyboardMarkup(
    one_time_keyboard=True,
    resize_keyboard=True
).add(types.KeyboardButton("Отлично! Идем дальше"))

# Удалить клавиатуру
delete_keyboard = types.ReplyKeyboardRemove()

# Покинуть маршрут
leave_keyboard = types.ReplyKeyboardMarkup(
    one_time_keyboard=True,
    resize_keyboard=True
).add(types.KeyboardButton("Покинуть маршрут"))
