import os

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import FSInputFile, Message
from dotenv import load_dotenv

import custom_keyboard
import messages

load_dotenv()

dirname = os.path.dirname(__file__)

# Число мест на каждом из маршрутов (возможно добавлять)
MAX_PLACES = (8, 6, 10)

router = Router()

# Счётчик маршрутов и мест с привязкой к id пользователя Telegram
way_counter = {}


class Cult_cuestions(StatesGroup):
    question_1 = State()
    raiting = State()


@router.message(Command('start'))
@router.message(F.text == 'Меню')
async def start_bot(message: Message):
    await message.answer(
        messages.WELCOME_MESSAGE,
    )
    await message.answer(
        messages.ABOUT_MESSAGE,
    )
    await message.answer(
        messages.START_MESSAGE,
    )
    await message.answer(
        messages.CHOISE_YOUR_WAY,
        reply_markup=custom_keyboard.keyboard_ways
    )
    way_counter[message.from_user.id] = [0, 0]
    return way_counter


@router.message(F.text == 'Завершить маршрут')
async def stop_journey(message: Message):
    await message.answer(
        messages.STOP_JOURNY,
        reply_markup=custom_keyboard.keyboard_menu
    )


@router.message(F.text == 'Нет')
async def not_start_place(message: Message):
    await message.answer(
        messages.MEDITATION_ADRESS
    )
    await message.answer(
            messages.ADDRESSES[way_counter[message.from_user.id][0]][
                way_counter[message.from_user.id][1] - 1]
        )
    await message.answer(
        messages.NOT_START_PLACE
    )
    await message.answer(
        messages.START_WAY_QUESTION,
        reply_markup=custom_keyboard.keyboard_yes_or_stop
    )


@router.message(F.text == 'О проекте')
async def about(message: Message):
    await message.answer(
        messages.ABOUT,
        reply_markup=custom_keyboard.keyboard_menu
    )


@router.message(F.text == 'Что ты умеешь?')
async def what_i_can_do(message: Message):
    await message.answer(
        messages.WHAT_I_CAN_DO,
        reply_markup=custom_keyboard.keyboard_menu
    )


@router.message(F.text == 'Маршрут 1. "Руки бы им оторвать"')
@router.message(F.text == 'Маршрут 2. "Не с кем играть. Играю со стенкой"')
@router.message(F.text == 'Маршрут 3. "… но спи/СМИ спокойно"')
async def choise_way(message: Message):
    maps = {
        'Маршрут 1. "Руки бы им оторвать"': '1.jpg',
        'Маршрут 2. "Не с кем играть. Играю со стенкой"': '2.jpg',
        'Маршрут 3. "… но спи/СМИ спокойно"': '3.jpg',
    }
    covers = {
        'Маршрут 1. "Руки бы им оторвать"': '1.jpg',
        'Маршрут 2. "Не с кем играть. Играю со стенкой"': '2.jpg',
        'Маршрут 3. "… но спи/СМИ спокойно"': '3.jpg',
    }
    ways = {
        'Маршрут 1. "Руки бы им оторвать"': 1,
        'Маршрут 2. "Не с кем играть. Играю со стенкой"': 2,
        'Маршрут 3. "… но спи/СМИ спокойно"': 3,
    }
    map_from_pc = FSInputFile(
        os.path.join(dirname, 'pictures', 'maps', maps[message.text])
    )
    cover_from_pc = FSInputFile(
        os.path.join(dirname, 'pictures', 'covers', covers[message.text])
    )
    way_counter[message.from_user.id][0] = int(ways[message.text])
    await message.answer_photo(
        cover_from_pc,
    )
    await message.answer(
        messages.WAY_DISCRIPTION[way_counter[message.from_user.id][0]]
    )
    await message.answer(
        messages.MAP_OF_WAY_BELOW
    )
    await message.answer_photo(
        map_from_pc,
    )
    await message.answer(
            messages.HOW_TO_PASS[way_counter[message.from_user.id][0]][0]
        )
    await message.answer(
        messages.START_WAY_QUESTION,
        reply_markup=custom_keyboard.keyboard_yes_no
    )
    return way_counter


@router.message(F.text == 'Да')
@router.message(F.text == 'Идём дальше!')
async def exhibit(message: Message, state: FSMContext):
    if way_counter[message.from_user.id][1] == 0:
        await message.answer(
            messages.START_MEDITATION
        )
    else:
        await message.answer(
            messages.MOVE_ON
        )
    if (
        way_counter[message.from_user.id][1] <
        MAX_PLACES[way_counter[message.from_user.id][0] - 1]
    ):
        way_counter[message.from_user.id][1] = (
            way_counter[message.from_user.id][1] + 1
        )

        await message.answer(
            messages.NAME_OF_PLACE[way_counter[message.from_user.id][0]][
                way_counter[message.from_user.id][1] - 1]
        )
        await message.answer(
            messages.ADDRESSES[way_counter[message.from_user.id][0]][
                way_counter[message.from_user.id][1] - 1]
        )
        await message.answer(
            messages.HOW_TO_PASS[way_counter[message.from_user.id][0]][
                way_counter[message.from_user.id][1] - 1]
        )
        # Если текст подводка есть
        if messages.INTRODUCTORY_TEXT[way_counter[message.from_user.id][0]][
                way_counter[message.from_user.id][1] - 1] != '':
            await message.answer(
                messages
                .INTRODUCTORY_TEXT[way_counter[message.from_user.id][0]][
                    way_counter[message.from_user.id][1] - 1]
            )
            await message.answer(messages.WRITE_YOUR_OPINION)
            # Ждём ввода текста
            await state.set_state(Cult_cuestions.question_1)
        # вариант, когда нет подводки
        else:
            await after_get_answer_1(message, state)
    else:
        await message.answer(
            messages.END_OF_WAY
        )
        await message.answer(
            messages.END_WAY_MESSAGE,
            reply_markup=custom_keyboard.keyboard_menu
        )


@router.message(Cult_cuestions.question_1)
async def after_get_answer_1(message: Message, state: FSMContext):
    picture = str(way_counter[message.from_user.id][1]) + '.jpg'
    image_from_pc = FSInputFile(
            os.path.join(
                dirname, 'pictures',
                str(way_counter[message.from_user.id][0]), picture
            )
        )
    await message.answer_photo(
        image_from_pc,
    )
    if (
        way_counter[message.from_user.id][0] == 1 and
        way_counter[message.from_user.id][1] == 1
    ):
        await message.answer_photo(
            FSInputFile(
                os.path.join(dirname, 'pictures', '1', '1_1.jpg')
            ),
        )
        await message.answer_photo(
            FSInputFile(
                os.path.join(dirname, 'pictures', '1', '1_2.jpg')
            ),
        )
        await message.answer_photo(
            FSInputFile(
                os.path.join(dirname, 'pictures', '1', '1_3.jpg')
            ),
        )
    if (
        way_counter[message.from_user.id][0] == 3 and
        way_counter[message.from_user.id][1] == 2
    ):
        await message.answer_photo(
            FSInputFile(
                os.path.join(dirname, 'pictures', '3', '2_1.jpg')
            ),
        )
    if (
        way_counter[message.from_user.id][0] == 3 and
        way_counter[message.from_user.id][1] == 10
    ):
        await message.answer_photo(
            FSInputFile(
                os.path.join(dirname, 'pictures', '3', '10_1.jpg')
            ),
        )
    await message.answer(
        messages
        .TEXT_PLACE[way_counter[message.from_user.id][0]][
            way_counter[message.from_user.id][1] - 1],
        parse_mode="HTML"
    )
    # вопрос для рефлексии
    if messages.AFTER_QUESTION[way_counter[message.from_user.id][0]][
            way_counter[message.from_user.id][1] - 1] != '':
        await message.answer(
            messages.AFTER_QUESTION[way_counter[message.from_user.id][0]][
                way_counter[message.from_user.id][1] - 1],
        )
    # ответ на рефлексию
    if messages.AFTER_ANSWER[way_counter[message.from_user.id][0]][
            way_counter[message.from_user.id][1] - 1] != '':
        await message.answer(
            messages.AFTER_ANSWER[way_counter[message.from_user.id][0]][
                way_counter[message.from_user.id][1] - 1]
        )
    # Оценка работы
    await message.answer(
        messages.RAITING_MESSAGE,
        reply_markup=custom_keyboard.keyboard_rating
    )
    # Ждём ввода текста
    await state.set_state(Cult_cuestions.raiting)
    # await message.answer(
    #     messages.GREAT,
    #     reply_markup=custom_keyboard.keyboard_go_on_or_stop
    # )
    return way_counter


@router.message(Cult_cuestions.raiting)
async def after_get_raiting(message: Message):
    await message.answer(
        messages.RAITING_THANKS,
        reply_markup=custom_keyboard.keyboard_go_on_or_stop
    )
