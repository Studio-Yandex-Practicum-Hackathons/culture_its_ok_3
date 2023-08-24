import os
import sys
from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import FSInputFile, Message
from dotenv import load_dotenv

from .custom_keyboard import *
from .messages import *
from .models import Profile, Route, Exhibit, ReviewOnExhibit, ReviewOnRoute, Journey

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
        START_MESSAGE,
        reply_markup=get_keyboard()
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
# @router.message(Command('map'))
async def choise_way(message: Message):
    print(message.text)

    pictures = {
        'Маршрут 1': r'pictures/way_1_map.jpg',
        'Маршрут 2': r'pictures/way_2_map.jpg',
        'Маршрут 3': r'pictures/way_3_map.jpg',
    }
    captions = {
        'Маршрут 1': 'Карта маршрута 1',
        'Маршрут 2': 'Карта маршрута 2',
        'Маршрут 3': 'Карта маршрута 3',
    }
    print(os.path.join(dirname, pictures[message.text]))
    image_from_pc = FSInputFile(
        os.path.join(dirname, pictures[message.text])
    )
    print(dirname)
    print(image_from_pc)
    way_counter[0] = int(message.text[-1])
    await message.answer(
        START_WAY_TEXT
    )
    await message.answer_photo(
        image_from_pc,
        caption=captions[message.text]
    )
    await message.answer(
        START_WAY_QUESTION,
        reply_markup=keyboard_yes_no
    )
    return way_counter


@router.message(F.text == 'Да')
@router.message(F.text == 'Идём дальше!')
# @router.message(Command('next'))
async def exhibit(message: Message):
    if way_counter[1] < MAX_PLACES:
        way_counter[1] = way_counter[1] + 1
        image_from_pc = FSInputFile(
            os.path.join(dirname, r'pictures\picture.jpg')
        )
        await message.answer(
            START_MEDITATION
        )
        await message.answer(
            TEXT_PLACE_1
        )
        await message.answer_photo(
            image_from_pc,
            caption="Фото экспоната"
        )
        await message.answer(
            EXHIBIT_INFO_1
        )
        await message.answer(
            QUESTION_ABOUT_EXHIBIT,
            reply_markup=keyboard_go_on_or_stop
        )
        return way_counter
    else:
        await message.answer(
            END_OF_WAY
        )
        await message.answer(
            END_WAY_MESSAGE,
            reply_markup=keyboard_menu
        )


@router.message(F.text == 'Завершить маршрут')
async def stop_journey(message: Message):
    await message.answer(
        STOP_JOURNY,
        reply_markup=keyboard_menu
    )


@router.message(F.text == 'Нет')
async def not_start_place(message: Message):
    await message.answer(
        NOT_START_PLACE
    )
    await message.answer(
        START_WAY_QUESTION,
        reply_markup=keyboard_yes_or_stop
    )


@router.message(F.text == 'О проекте')
async def about(message: Message):
    await message.answer(
        ABOUT,
        reply_markup=keyboard_menu
    )


@router.message(F.text == 'Что ты умеешь?')
async def what_i_can_do(message: Message):
    await message.answer(
        WHAT_I_CAN_DO,
        reply_markup=keyboard_menu
    )


# ----------------------
@router.message(Command('count'))
async def do_count(message: Message):
    chat_id = message.from_user.id

    p, _ = Profile.objects.get_or_create(
        external_id=chat_id,
        defaults={
            'name': message.from_user.first_name,
        }
    )
    count = Message.objects.filter(profile=p).count()

    # count = 0
    await message.answer(
        text=f'У вас {count} сообщений',
    )


@router.message(Command('next'))
async def do_next(message: Message):
    chat_id = message.from_user.id

    tr = Journey.objects.get(traveler=chat_id)
    if tr.now_exhibit < Route.objects.get(title=tr.route.title).exhibit.count():
        ex = Exhibit.objects.get(route__title=tr.route, order=tr.now_exhibit + 1)
        tr.now_exhibit = tr.now_exhibit + 1
        tr.save()
        await message.answer(
            text=ex.description,
        )
        path = os.path.join(dirname, str(ex.image).replace('excursion/'))
        image_from_pc = FSInputFile(path)
        print(image_from_pc)
        await message.answer_photo(
            image_from_pc,
            caption="фотка экспоната"
        )

    else:
        tr.delete()
        await message.answer(
            text='это было прекрасно',
        )



@router.message(Command('map'))
async def do_map(message: Message):
    chat_id = message.from_user.id
    print(chat_id)
    number_map = str(message.text).split()[1]
    Journey.objects.filter(traveler=chat_id).delete()
    print(Route.objects.get(title=number_map).exhibit.count())
    tr = Journey(
        traveler=chat_id,
        route=Route.objects.get(title=number_map),
        now_exhibit=0
    )
    tr.save()

    await message.answer(
        text='Ну что погнали !',
    )

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

@router.message(Command('v'))
async def do_next(message: Message):
    chat_id = message.from_user.id

    path = os.path.join(dirname, 'pictures/IMG_6528.mp4')
    print(path)
    image_from_pc = FSInputFile(path)
    print(image_from_pc)
    await message.answer_video(
        image_from_pc,
        caption="фотка экспоната"
    )

@router.message(Command('a'))
async def do_next(message: Message):
    chat_id = message.from_user.id

    path = os.path.join(dirname, 'pictures/9.Гороховый бранль.mp3')
    print(path)
    image_from_pc = FSInputFile(path)
    print(image_from_pc)
    await message.answer_audio(
        image_from_pc,
        caption="фотка экспоната"
    )

@router.message(Command('list'))
async def do_next(message: Message):
    chat_id = message.from_user.id
    list_rout = Route.objects.all()

    path = os.path.join(dirname, 'pictures/9.Гороховый бранль.mp3')
    print(path)
    image_from_pc = FSInputFile(path)
    print(image_from_pc)
    for r in list_rout:
        await message.answer(
            text=r.title
        )

@router.message()
async def what_i_can_do(message: Message):
    chat_id = message.from_user.id

    try:
        f = Journey.objects.get(traveler=chat_id)  # MultipleObjectsReturned
        print(f)
    except ObjectDoesNotExist:
        print("Объект не сушествует")
        return None
    except MultipleObjectsReturned:
        print("Найдено более одного объекта")
        return None

    await message.answer(
        text='эхооооо'
    )


