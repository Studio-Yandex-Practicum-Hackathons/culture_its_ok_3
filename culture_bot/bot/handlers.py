import os

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import FSInputFile, Message
from dotenv import load_dotenv

import custom_keyboard
import messages

load_dotenv()

dirname = os.path.dirname(__file__)

# Число мест на каждом из маршрутов (возможно добавлять)
MAX_PLACES = (8, 3, 3)

router = Router()

# Счётчик маршрутов и мест с привязкой к id пользователя Telegram
way_counter = {}


@router.message(Command('start'))
@router.message(F.text == 'Меню')
async def start_bot(message: Message):
    image_from_pc = FSInputFile(
        os.path.join(dirname, 'pictures', 'map.jpg')
    )
    await message.answer(
        messages.START_MESSAGE,
        reply_markup=custom_keyboard.keyboard_ways
    )
    await message.answer_photo(
        image_from_pc,
        caption="Карта фестиваля"
    )

    way_counter[message.from_user.id] = [0, 0]
    return way_counter


@router.message(F.text == 'Маршрут 1. "Руки бы им оторвать"')
@router.message(F.text == 'Маршрут 2')
@router.message(F.text == 'Маршрут 3')
async def choise_way(message: Message):
    pictures = {
        'Маршрут 1. "Руки бы им оторвать"': 'way_1_map.jpg',
        'Маршрут 2': 'way_2_map.jpg',
        'Маршрут 3': 'way_3_map.jpg',
    }
    captions = {
        'Маршрут 1. "Руки бы им оторвать"': 'Карта маршрута 1',
        'Маршрут 2': 'Карта маршрута 2',
        'Маршрут 3': 'Карта маршрута 3',
    }
    ways = {
        'Маршрут 1. "Руки бы им оторвать"': 1,
        'Маршрут 2': 2,
        'Маршрут 3': 3,
    }
    image_from_pc = FSInputFile(
        os.path.join(dirname, 'pictures', pictures[message.text])
    )
    way_counter[message.from_user.id][0] = int(ways[message.text])
    await message.answer(
        messages.START_WAY_TEXT
    )
    await message.answer_photo(
        image_from_pc,
        caption=captions[message.text]
    )
    await message.answer(
        messages.START_WAY_QUESTION,
        reply_markup=custom_keyboard.keyboard_yes_no
    )
    return way_counter


@router.message(F.text == 'Да')
@router.message(F.text == 'Идём дальше!')
async def exhibit(message: Message):
    if (
        way_counter[message.from_user.id][1] <
        MAX_PLACES[way_counter[message.from_user.id][0] - 1]
    ):
        way_counter[message.from_user.id][1] = (
            way_counter[message.from_user.id][1] + 1
        )
        picture = str(way_counter[message.from_user.id][1]) + '.jpg'
        image_from_pc = FSInputFile(
            os.path.join(
                dirname, 'pictures',
                str(way_counter[message.from_user.id][0]), picture
            )
        )
        await message.answer(
            messages.START_MEDITATION
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
        await message.answer(
            messages
            .TEXT_PLACE_1[way_counter[message.from_user.id][0]][
                way_counter[message.from_user.id][1] - 1]
        )
        await message.answer_photo(
            image_from_pc,
        )
        await message.answer(
            messages.QUESTION_ABOUT_EXHIBIT,
            reply_markup=custom_keyboard.keyboard_go_on_or_stop
        )
        return way_counter
    else:
        await message.answer(
            messages.END_OF_WAY
        )
        await message.answer(
            messages.END_WAY_MESSAGE,
            reply_markup=custom_keyboard.keyboard_menu
        )


@router.message(F.text == 'Завершить маршрут')
async def stop_journey(message: Message):
    await message.answer(
        messages.STOP_JOURNY,
        reply_markup=custom_keyboard.keyboard_menu
    )


@router.message(F.text == 'Нет')
async def not_start_place(message: Message):
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
