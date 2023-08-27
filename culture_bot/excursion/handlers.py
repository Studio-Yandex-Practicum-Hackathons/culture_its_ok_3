import os
import sys

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import FSInputFile, Message
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from dotenv import load_dotenv

from .custom_keyboard import *
from .messages import *
from .models import Exhibit, Journey, ReflectionExhibit, Route

load_dotenv()

dirname = os.path.dirname(__file__)


router = Router()

way_counter = [0, 0]


class Cult_cuestions(StatesGroup):
    question_1 = State()
    raiting = State()

@router.message(Command('start'))
@router.message(F.text == 'Меню')
async def start_bot(message: Message):
    await message.answer(
        START_MESSAGE,
        reply_markup=keyboard_ways
    )

    image_from_pc = FSInputFile(
        os.path.join(dirname, r'pictures\map.jpg')
    )
    await message.answer_photo(
        image_from_pc,
        caption="Карта фестиваля"
    )
    await message.answer(
        WELCOME_MESSAGE,
    )
    await message.answer(
        ABOUT_MESSAGE,
    )
    await message.answer(
        START_MESSAGE,
    )
    await message.answer(
        CHOISE_YOUR_WAY,
        reply_markup=keyboard_ways
    )


@router.message(F.text == 'Завершить маршрут')
async def stop_journey(message: Message):
    await message.answer(STOP_JOURNY, reply_markup=keyboard_menu)

@router.message(Cult_cuestions.raiting)
async def after_get_raiting(message: Message):
    await message.answer(RAITING_THANKS, reply_markup=keyboard_go_on_or_stop)


# если находимся не рядом с местом медитации
@router.message(F.text == 'Нет')
async def not_start_place(message: Message):

    await message.answer(MEDITATION_ADRESS)
    await message.answer(ADDRESSES[way_counter[message.from_user.id][0]][way_counter[message.from_user.id][1] - 1])
    await message.answer(NOT_START_PLACE)
    await message.answer(START_WAY_QUESTION, reply_markup=keyboard_yes_or_stop)

@router.message(F.text == 'О проекте')
async def about(message: Message):
    await message.answer(ABOUT, reply_markup=keyboard_menu)


@router.message(F.text == 'Что ты умеешь?')
async def what_i_an_do(message: Message):
    await message.answer(WHAT_I_CAN_DO, reply_markup=keyboard_menu)

@router.message(F.text == 'Да')
@router.message(F.text == 'Идём дальше!')
@router.message(Command('next'))
async def do_next(message: Message):
    chat_id = message.from_user.id

    tr = Journey.objects.get(traveler=chat_id)
    if tr.now_exhibit < Route.objects.get(title=tr.route.title).exhibit.count():
        ex = Exhibit.objects.get(route__title=tr.route, order=tr.now_exhibit + 1)

        tr.now_exhibit = tr.now_exhibit + 1
        tr.save()

        for i in ex.description_exhibit.all():
            await message.answer(text=i.text)

        # отправка нескольких фоток
        try:
            if ex.photo_exhibit.count() > 0:
                for i in ex.photo_exhibit.all():
                    path = os.path.join(dirname, str(i.photo).replace('excursion/', ''))
                    image_from_pc = FSInputFile(path)
                    caption = i.description if i.description else ''
                    await message.answer_photo(
                        image_from_pc,
                        caption=caption
                    )
        except:
            pass

        # отправка аудио
        try:
            if ex.audio_exhibit.count() > 0:
                for i in ex.audio_exhibit.all():
                    path = os.path.join(dirname, str(i.photo).replace('excursion/', ''))
                    audio_from_pc = FSInputFile(path)
                    await message.answer_audio(
                        audio_from_pc,
                    )
        except:
            pass

        # отправка видео
        try:
            if ex.video_exhibit.count() > 0:
                for i in ex.video_exhibit.all():
                    path = os.path.join(dirname, str(i.photo).replace('excursion/', ''))
                    video_from_pc = FSInputFile(path)
                    await message.answer_audio(
                        video_from_pc,
                    )
        except:
            pass

        await message.answer(text=ex.question_for_reflection)

    else:
        tr.delete()
        await message.answer(
            END_OF_WAY
        )

        # ссылка на форму обратной связи
        await message.answer(
            END_WAY_MESSAGE,
            reply_markup=keyboard_menu
        )


@router.message(Command('map'))
async def do_map(message: Message):
    chat_id = message.from_user.id

    number_map = str(message.text).replace('/map ', '')

    Journey.objects.filter(traveler=chat_id).delete()
    tr = Journey(
        traveler=chat_id,
        route=Route.objects.get(title=number_map),
        now_exhibit=0
    )
    tr.save()

    route = Route.objects.get(title=number_map)
    cover = FSInputFile(os.path.join(dirname, str(route.cover).replace('excursion/', '')))
    await message.answer_photo(
        cover,
        caption=route.title
    )
    await message.answer(
        text=route.lyrics
    )
    await message.answer(
        text=route.description,
    )

    await message.answer(MAP_OF_WAY_BELOW)
    route_map = FSInputFile(os.path.join(dirname, str(route.route_map).replace('excursion/', '')))
    await message.answer_photo(
        route_map, caption=f'Карта маршрута {route.title}'
    )

    # как пройти к началу
    await message.answer(route.where_start)

    # 'Вы на месте?'
    await message.answer(START_WAY_QUESTION)

    return way_counter


@router.message()
async def free_communication(message: Message):
    user = message.from_user

    try:
        travel = Journey.objects.get(traveler=user.id)
        if travel.now_exhibit:
            ReflectionExhibit(
                exhibit=Exhibit.objects.get(route=travel.route, order=travel.now_exhibit),
                author=user.username,
                contact=user.id,
                text=message.text
            ).save()

        # ответ на рефлексию
        await message.answer(
            text=Exhibit.objects.get(route=travel.route, order=travel.now_exhibit).answer_for_reflection
        )

        return None

    except ObjectDoesNotExist:
        print("Объект не сушествует")
        return None
    except MultipleObjectsReturned:
        print("Найдено более одного объекта")
        return None
    #
    # await message.answer(
    #     text='Спасибо, за ваш отзыв!'
    # )

    # # Оценка работы
    # await message.answer(RAITING_MESSAGE, reply_markup=keyboard_rating)
    #
    # # супер
    # await message.answer(GREAT, reply_markup=keyboard_go_on_or_stop)
    # return way_counter

#------------------
# @router.message(Command('count'))
# async def do_count(message: Message):
#     chat_id = message.from_user.id
#
#     p, _ = Profile.objects.get_or_create(
#         external_id=chat_id,
#         defaults={
#             'name': message.from_user.first_name,
#         }
#     )
#     count = Message.objects.filter(profile=p).count()
#
#     # count = 0
#     await message.answer(
#         text=f'У вас {count} сообщений',
#     )
#
# @router.message(Command('list'))
# async def do_list(message: Message):
#     chat_id = message.from_user.id
#     list_rout = Route.objects.all()
#
#     path = os.path.join(dirname, 'pictures/9.Гороховый бранль.mp3')
#     print(path)
#     image_from_pc = FSInputFile(path)
#     print(image_from_pc)
#     for r in list_rout:
#         await message.answer(
#             text=r.title
#         )
#
# @router.message(Command('a'))
# async def do_audio(message: Message):
#     chat_id = message.from_user.id
#
#     path = os.path.join(dirname, 'pictures/9.Гороховый бранль.mp3')
#     print(path)
#     image_from_pc = FSInputFile(path)
#     print(image_from_pc)
#     await message.answer_audio(
#         image_from_pc,
#         caption="фотка экспоната"
#     )
#
# @router.message(Command('v'))
# async def do_next(message: Message):
#     chat_id = message.from_user.id
#
#     path = os.path.join(dirname, 'pictures/IMG_6528.mp4')
#     print(path)
#     image_from_pc = FSInputFile(path)
#     print(image_from_pc)
#     await message.answer_video(
#         image_from_pc,
#         caption="фотка экспоната"
#     )