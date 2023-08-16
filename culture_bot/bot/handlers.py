import os

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import FSInputFile, Message
from dotenv import load_dotenv

import custom_keyboard
import messages

load_dotenv()

dirname = os.path.dirname(__file__)

MAX_PLACES = 3

router = Router()

way_counter = [0, 0]


@router.message(Command('start'))
@router.message(F.text == 'Меню')
async def start_bot(message: Message):
    image_from_pc = FSInputFile(
        os.path.join(dirname, r'pictures\map.jpg')
    )
    await message.answer(
        messages.START_MESSAGE,
        reply_markup=custom_keyboard.keyboard_ways
    )
    await message.answer_photo(
        image_from_pc,
        caption="Карта фестиваля"
    )
    way_counter[0] = 0
    way_counter[1] = 0
    return way_counter


@router.message(F.text == 'Маршрут 1')
@router.message(F.text == 'Маршрут 2')
@router.message(F.text == 'Маршрут 3')
async def choise_way(message: Message):
    pictures = {
        'Маршрут 1': r'pictures\way_1_map.jpg',
        'Маршрут 2': r'pictures\way_2_map.jpg',
        'Маршрут 3': r'pictures\way_3_map.jpg',
    }
    captions = {
        'Маршрут 1': 'Карта маршрута 1',
        'Маршрут 2': 'Карта маршрута 2',
        'Маршрут 3': 'Карта маршрута 3',
    }
    image_from_pc = FSInputFile(
        os.path.join(dirname, pictures[message.text])
    )
    way_counter[0] = int(message.text[-1])
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
    if way_counter[1] < MAX_PLACES:
        way_counter[1] = way_counter[1] + 1
        image_from_pc = FSInputFile(
            os.path.join(dirname, r'pictures\picture.jpg')
        )
        await message.answer(
            messages.START_MEDITATION
        )
        await message.answer(
            messages.TEXT_PLACE_1
        )
        await message.answer_photo(
            image_from_pc,
            caption="Фото экспоната"
        )
        await message.answer(
            messages.EXHIBIT_INFO_1
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
