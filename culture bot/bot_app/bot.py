from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext

# Токен бота и сообщение при нажатии кнопки старт
TOKEN_API = '########'
MESSAGE = """ Привет! Какой маршрут выберете?
Описание маршрутов можно найти в bio к боту. """

# Память, в которой будет храниться текущее состояние бота (RouteStatesGroup)
storage = MemoryStorage()

bot = Bot(TOKEN_API)
dp = Dispatcher(bot, storage=storage)


# Состояния бота
class RouteStatesGroup(StatesGroup):
    m1 = State()  # При выборе маршрута 1
    m2 = State()  # При выборе маршрута 2
    m3 = State()  # При выборе маршрута 3
    m1_review1 = State()  # Промежуточное состояние, когда пользователь пишет отзыв на экспонат маршрута 1 экспонтата 1
    m2_review1 = State()  # Промежуточное состояние, когда пользователь пишет отзыв на экспонат маршрута 2 экспонтата 1
    m3_review1 = State()  # Промежуточное состояние, когда пользователь пишет отзыв на экспонат маршрута 3 экспонтата 1
    m1_answer1 = State()  # Промежуточное состояние, Ответ пользователю на экспонат маршрута 1 экспонтата 1, описание экспоната 2
    m2_answer1 = State()  # Промежуточное состояние, Ответ пользователю на экспонат маршрута 2 экспонтата 1, описание экспоната 2
    m3_answer1 = State()  # Промежуточное состояние, Ответ пользователю на экспонат маршрута 3 экспонтата 1, описание экспоната 2
    the_end = State()  # Маршрут подходит к концу


# При нажатии кнопки старт
@dp.message_handler(
    commands=['start'],
    state=[None, RouteStatesGroup.m1, RouteStatesGroup.m2,
           RouteStatesGroup.m3, RouteStatesGroup.m1_review1,
           RouteStatesGroup.m2_review1, RouteStatesGroup.m3_review1,
           RouteStatesGroup.m1_answer1, RouteStatesGroup.m2_answer1,
           RouteStatesGroup.m3_answer1, RouteStatesGroup.the_end]
)
async def start(message: types.Message, state: FSMContext):
    button_1 = types.InlineKeyboardButton(text="Маршрут 1")
    button_2 = types.InlineKeyboardButton(text="Маршрут 2")
    button_3 = types.InlineKeyboardButton(text="Маршрут 3")
    keyboard = types.ReplyKeyboardMarkup(
        resize_keyboard=True,
        input_field_placeholder="Выберите способ"
    )
    keyboard.add(button_1).add(button_2).add(button_3)
    await state.finish()
    await message.answer(
        text=MESSAGE,
        reply_markup=keyboard
    )


# При нажатии кнопки 'Покинуть маршрут'
@dp.message_handler(
    text="Покинуть маршрут",
    state=[None, RouteStatesGroup.m1, RouteStatesGroup.m2,
           RouteStatesGroup.m3, RouteStatesGroup.m1_review1,
           RouteStatesGroup.m2_review1, RouteStatesGroup.m3_review1,
           RouteStatesGroup.m1_answer1, RouteStatesGroup.m2_answer1,
           RouteStatesGroup.m3_answer1, RouteStatesGroup.the_end]
)
async def cmd_start(message: types.Message, state: FSMContext):
    button_1 = types.InlineKeyboardButton(text="Маршрут 1")
    button_2 = types.InlineKeyboardButton(text="Маршрут 2")
    button_3 = types.InlineKeyboardButton(text="Маршрут 3")
    keyboard = types.ReplyKeyboardMarkup(
        resize_keyboard=True,
        input_field_placeholder="Выберите способ", one_time_keyboard=True
    )
    keyboard.add(button_1).add(button_2).add(button_3)
    await state.finish()
    await message.answer(text="Выберите маршрут", reply_markup=keyboard)


# При наатии кнопки 'Нет, не готов'
@dp.message_handler(
    text="Нет, не готов",
    state=[None, RouteStatesGroup.m1, RouteStatesGroup.m2,
           RouteStatesGroup.m3, RouteStatesGroup.m1_review1,
           RouteStatesGroup.m2_review1, RouteStatesGroup.m3_review1,
           RouteStatesGroup.m1_answer1, RouteStatesGroup.m2_answer1,
           RouteStatesGroup.m3_answer1, RouteStatesGroup.the_end]
)
async def m_1(message: types.Message):
    button_1 = types.KeyboardButton(text="Возобновить прохождение маршрута")
    button_2 = types.KeyboardButton(text="Покинуть маршрут")
    keyboard = types.ReplyKeyboardMarkup(
        resize_keyboard=True,
        input_field_placeholder="Выберите способ"
    )
    keyboard.add(button_1).add(button_2)
    await message.answer(
        "Вы хотите...",
        reply_markup=keyboard
    )


# При выборе первого маршрута
@dp.message_handler(text="Маршрут 1")
async def m_1(message: types.Message):
    global route
    route = "first"
    kb = [
        [
            types.KeyboardButton(text="Начнем"),
            types.KeyboardButton(text="Нет, не готов")
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выберите способ"
    )
    await RouteStatesGroup.m1.set()
    await message.answer('*Приветственное сообщение')
    await message.answer("Вы готовы начать?", reply_markup=keyboard)
    await bot.send_photo(chat_id=message.chat.id,
                         photo="https://ibb.co/WKTXjmd")


# При выборе второго маршрута
@dp.message_handler(text="Маршрут 2")
async def m_2(message: types.Message):
    kb = [
        [
            types.KeyboardButton(text="Начнем"),
            types.KeyboardButton(text="Нет, не готов")
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выберите способ"
    )
    await RouteStatesGroup.m2.set()
    await message.answer('*Приветственное сообщение')
    await message.answer("Вы готовы начать?", reply_markup=keyboard)
    await bot.send_photo(
        chat_id=message.chat.id,
        photo="https://rossaprimavera.ru/static/files/372a48d070ef.jpg"
    )


# При выборе третьего маршрута
@dp.message_handler(text="Маршрут 3")
async def m_3(message: types.Message):
    kb = [
        [
            types.KeyboardButton(text="Начнем"),
            types.KeyboardButton(text="Нет, не готов")
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выберите способ"
    )
    await RouteStatesGroup.m3.set()
    await message.answer('*Приветственное сообщение')
    await message.answer("Вы готовы начать?", reply_markup=keyboard)
    await bot.send_photo(
        chat_id=message.chat.id,
        photo="https://rossaprimavera.ru/static/files/02c815cc55b1.jpg"
    )


# При нажатии на кнопки 'Начнем', 'Возобновить прохождение маршрута 1'
@dp.message_handler(
    text=("Начнем", "Возобновить прохождение маршрута"),
    state=RouteStatesGroup.m1
)
async def m_1(message: types.Message):
    kb = [
        [
            types.KeyboardButton(text="Да"),
            types.KeyboardButton(text="Нет")
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Находитесь вы в этом месте?"
    )
    await message.answer("Находитесь вы в этом месте?")  # Уточняющий вопрос про место
    await bot.send_photo(
        caption="Улица Маяковского дом 9",
        reply_markup=keyboard,
        photo="https://crossarea.ru/wp-content/uploads/"
        "2018/07/street-art-graffiti-800x534.png",
        chat_id=message.chat.id
    )


# При нажатии на кнопки 'Начнем', 'Возобновить прохождение маршрута 2'
@dp.message_handler(
    text=("Начнем", "Возобновить прохождение маршрута"),
    state=RouteStatesGroup.m2
)
async def m_2(message: types.Message):
    kb = [
        [
            types.KeyboardButton(text="Да"),
            types.KeyboardButton(text="Нет")
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Находитесь вы в этом месте?"
    )
    await message.answer("Находитесь вы в этом месте?")
    await bot.send_photo(
        caption="Улица Пушкина дом 25",
        reply_markup=keyboard,
        photo="https://encrypted-tbn0.gstatic.com/images?q=tbn"
        ":ANd9GcResQ81fViuOGiyZUN-Z1463n5rfbNR9aX8UOFhDWgedw&s",
        chat_id=message.chat.id
    )


# При нажатии на кнопки 'Начнем', 'Возобновить прохождение маршрута 3'
@dp.message_handler(
    text=("Начнем", "Возобновить прохождение маршрута"),
    state=RouteStatesGroup.m3
)
async def m_3(message: types.Message):
    kb = [
        [
            types.KeyboardButton(text="Да"),
            types.KeyboardButton(text="Нет")
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Находитесь вы в этом месте?"
    )
    await message.answer("Находитесь вы в этом месте?")
    await bot.send_photo(
        caption="Улица Асадова дом 7",
        reply_markup=keyboard,
        photo="https://www.archnadzor.ru/wp-content/"
        "uploads/2019/02/Dokuchaev-per-10.jpg",
        chat_id=message.chat.id
    )


# Если пользователь не на указанном месте, бот скидывает фото карт и локацию
# Ссылку на яндекс карты пока не добавлял
@dp.message_handler(text="Нет", state=RouteStatesGroup.m1)
async def m_1(message: types.Message):
    kb = [
        [
            types.KeyboardButton(text="Я на месте."),
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выберите способ"
    )
    await bot.send_photo(
        caption="Вам нужно пройти вот сюда",
        chat_id=message.chat.id,
        photo="https://ibb.co/y0gZdvw"
    )
    await bot.send_location(
        chat_id=message.chat.id,
        latitude=55.592388,
        longitude=38.123072,
        reply_markup=keyboard
    )


# Если пользователь не на указанном месте, бот скидывает фото карт и локацию
# Ссылку на яндекс карты пока не добавлял
@dp.message_handler(text="Нет", state=RouteStatesGroup.m2)
async def m_2(message: types.Message):
    kb = [
        [
            types.KeyboardButton(text="Я на месте."),
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выберите способ"
    )
    await bot.send_photo(
        caption="Вам нужно пройти вот сюда",
        chat_id=message.chat.id,
        photo="https://appassets.mvtdev.com/map/137/s/902/15577227.jpg"
    )
    await bot.send_location(
        chat_id=message.chat.id,
        latitude=28.592388,
        longitude=17.123072,
        reply_markup=keyboard
    )


# Если пользователь не на указанном месте, бот скидывает фото карт и локацию
# Ссылку на яндекс карты пока не добавлял
@dp.message_handler(text="Нет", state=RouteStatesGroup.m3)
async def m_3(message: types.Message):
    kb = [
        [
            types.KeyboardButton(text="Я на месте."),
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выберите способ"
    )
    await bot.send_photo(
        caption="Вам нужно пройти вот сюда",
        chat_id=message.chat.id,
        photo="https://www.moscowmap.ru/_public/mmap/"
        "house/0005/71/59-ul-sedova-5-korp-1.png"
    )
    await bot.send_location(
        chat_id=message.chat.id,
        latitude=72.592388,
        longitude=27.123072,
        reply_markup=keyboard
    )


# Если пользователь подтвердил, что готов к прохождению маршрута, бот
# скидывает первый экспонат маршрута 1
@dp.message_handler(text=("Да", "Я на месте."), state=RouteStatesGroup.m1)
async def m_1_rewiews(message: types.Message):
    await bot.send_photo(
        chat_id=message.chat.id,
        photo="https://upload.wikimedia.org/wikipedia/"
        "commons/thumb/6/68/Alien_Girl.jpg/220px-Alien_Girl.jpg",
        caption="Опишите свои впечатления",
        reply_markup=types.ReplyKeyboardRemove()
    )
    await RouteStatesGroup.m1_review1.set()  # Бот ждёт ответа от пользователя


# Если пользователь подтвердил, что готов к прохождению маршрута, бот
# скидывает первый экспонат маршрута 2
@dp.message_handler(text=("Да", "Я на месте."), state=RouteStatesGroup.m2)
async def m_2_rewiews(message: types.Message):
    await bot.send_photo(
        chat_id=message.chat.id,
        photo="https://artguide.com/uploads/"
        "ckeditor/pictures/590/content_01.jpg",
        caption="Опишите свои впечатления",
        reply_markup=types.ReplyKeyboardRemove()
    )
    await RouteStatesGroup.m2_review1.set()  # Бот ждёт ответа от пользователя


# Если пользователь подтвердил, что готов к прохождению маршрута, бот
# скидывает первый экспонат маршрута 3
@dp.message_handler(text=("Да", "Я на месте."), state=RouteStatesGroup.m3)
async def m_3_rewiews(message: types.Message):
    await bot.send_photo(
        chat_id=message.chat.id,
        photo="https://storage.yandexcloud.net/"
        "moskvichmag/uploads/2022/09/graf1.jpg",
        caption="Опишите свои впечатления",
        reply_markup=types.ReplyKeyboardRemove()
    )
    await RouteStatesGroup.m3_review1.set()  # Бот ждёт ответа от пользователя


# Бот получает ответ от пользователя
@dp.message_handler(state=RouteStatesGroup.m1_review1)
async def m_1_rewiews(message: types.Message):
    await message.reply("Как интересно")
    await message.answer(
        "Нажми кнопку 'Отлично! Идем дальше',"
        "чтобы перейти к следующей экспозиции.",
        reply_markup=types.ReplyKeyboardMarkup(
            resize_keyboard=True)
        .add(types.KeyboardButton("Отлично! Идем дальше")))
    await RouteStatesGroup.m1_answer1.set()


# Бот получает ответ от пользователя
@dp.message_handler(state=RouteStatesGroup.m2_review1)
async def m_2_rewiews(message: types.Message):
    await message.reply("Как интересно")
    await message.answer(
        "Нажми кнопку 'Отлично! Идем дальше',"
        "чтобы перейти к следующей экспозиции.",
        reply_markup=types.ReplyKeyboardMarkup(
            resize_keyboard=True)
        .add(types.KeyboardButton("Отлично! Идем дальше")))
    await RouteStatesGroup.m2_answer1.set()


# Бот получает ответ от пользователя
@dp.message_handler(state=RouteStatesGroup.m3_review1)
async def m_3_rewiews(message: types.Message):
    await message.reply("Как интересно")
    await message.answer(
        "Нажми кнопку 'Отлично! Идем дальше',"
        "чтобы перейти к следующей экспозиции.",
        reply_markup=types.ReplyKeyboardMarkup(
            resize_keyboard=True)
        .add(types.KeyboardButton("Отлично! Идем дальше")))
    await RouteStatesGroup.m3_answer1.set()


# Бот описывает второй экспонат маршрута 1
@dp.message_handler(text="Отлично! Идем дальше",
                    state=RouteStatesGroup.m1_answer1)
async def m_1_rewiews(message: types.Message):
    await bot.send_photo(
        chat_id=message.chat.id,
        photo="https://s9.travelask.ru/uploads/post/"
        "000/003/101/main_image/full-24d89de5236f001171085f9a6ad6a2c3.jpg",
        caption="Опишите свои впечатления",
        reply_markup=types.ReplyKeyboardRemove()
    )
    await RouteStatesGroup.the_end.set()  # Экспонаты закончились


# Бот описывает второй экспонат маршрута 2
@dp.message_handler(text="Отлично! Идем дальше",
                    state=RouteStatesGroup.m2_answer1)
async def m_2_rewiews(message: types.Message):
    await bot.send_photo(
        chat_id=message.chat.id,
        photo="https://crossarea.ru/wp-content/"
        "uploads/2018/07/Vhils-street-art-800x515.jpg",
        caption="Опишите свои впечатления",
        reply_markup=types.ReplyKeyboardRemove()
    )
    await RouteStatesGroup.the_end.set()  # Экспонаты закончились


# Бот описывает второй экспонат маршрута 3
@dp.message_handler(text="Отлично! Идем дальше",
                    state=RouteStatesGroup.m3_answer1)
async def m_3_rewiews(message: types.Message):
    await bot.send_photo(
        chat_id=message.chat.id,
        photo="https://encrypted-tbn0.gstatic.com/images?"
        "q=tbn:ANd9GcSNSDkNdSXDW8bW9KaHeVTRIrLLnC1iy5oq5w&usqp=CAU",
        caption="Опишите свои впечатления",
        reply_markup=types.ReplyKeyboardRemove()
    )
    await RouteStatesGroup.the_end.set()  # Экспонаты закончились


# Последнее сообщение бота по маршруту, форма для отзывов и кнопка возврата к выбору маршрута
@dp.message_handler(state=RouteStatesGroup.the_end)
async def the_end(message: types.Message):
    await message.answer(
        "Конец",
        reply_markup=types.ReplyKeyboardMarkup(
            resize_keyboard=True)
        .add(types.KeyboardButton("Покинуть маршрут")))
    await RouteStatesGroup.the_end.set()


if __name__ == '__main__':
    executor.start_polling(dp)
