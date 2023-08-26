import os
import sys

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import FSInputFile, Message
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from dotenv import load_dotenv

from .custom_keyboard import *
from .messages import *
from .models import (Exhibit, Journey, Profile, ReviewOnExhibit, ReviewOnRoute,
                     Route)

load_dotenv()

dirname = os.path.dirname(__file__)

MAX_PLACES = (8, 6, 10)

router = Router()

way_counter = [0, 0]

class Cult_cuestions(StatesGroup):
    question_1 = State()
    raiting = State()

@router.message(Command('start'))
@router.message(F.text == 'Меню')
async def start_bot(message: Message):
    image_from_pc = FSInputFile(
        os.path.join(dirname, r'pictures\map.jpg')
    )
    await message.answer(
        START_MESSAGE,
        reply_markup=keyboard_ways
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
    way_counter[message.from_user.id] = [0, 0]
    return way_counter


@router.message(F.text == 'Маршрут 1. "Руки бы им оторвать"')
@router.message(F.text == 'Маршрут 2. "Не с кем играть. Играю со стенкой"')
@router.message(F.text == 'Маршрут 3. "… но спи/СМИ спокойно"')
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

    print(os.path.join(dirname, pictures[message.text]))
    image_from_pc = FSInputFile(
        os.path.join(dirname, pictures[message.text])
    )
    print(dirname)
    print(image_from_pc)
    way_counter[0] = int(message.text[-1])
    await message.answer(START_WAY_TEXT)
    await message.answer_photo(
        image_from_pc,
        caption=captions[message.text]
    )
    await message.answer(
        START_WAY_QUESTION,
        reply_markup=keyboard_yes_no
    )
    #
    map_from_pc = FSInputFile(
        os.path.join(dirname, 'pictures', 'maps', maps[message.text])
    )
    cover_from_pc = FSInputFile(
        os.path.join(dirname, 'pictures', 'covers', covers[message.text])
    )
    way_counter[message.from_user.id][0] = int(ways[message.text])

    # отправка картинки маршрута
    await message.answer_photo(cover_from_pc,)

    # описание маршрута
    await message.answer(WAY_DISCRIPTION[way_counter[message.from_user.id][0]])

    # Ниже представлена карта маршрута:
    await message.answer(MAP_OF_WAY_BELOW)

    # отправка карты маршрута
    await message.answer_photo(
        map_from_pc,
    )

    # как пройти к началу
    await message.answer(
        HOW_TO_PASS[way_counter[message.from_user.id][0]][0]
    )

    # 'Вы на месте?'
    await message.answer(
        START_WAY_QUESTION,
        reply_markup=keyboard_yes_no
    )

    return way_counter


@router.message(F.text == 'Да')
@router.message(F.text == 'Идём дальше!')
async def exhibit(message: Message, state: FSMContext):
    if way_counter[message.from_user.id][1] == 0:
        # начало медитации
        await message.answer(START_MEDITATION)
    else:
        # идем дальше
        await message.answer(MOVE_ON)

    # проверка конец ли это маршрута или нет
    if (way_counter[message.from_user.id][1] < MAX_PLACES[way_counter[message.from_user.id][0] - 1]):
        way_counter[message.from_user.id][1] = (
            way_counter[message.from_user.id][1] + 1
        )

        # название места
        await message.answer(
            NAME_OF_PLACE[way_counter[message.from_user.id][0]][
                way_counter[message.from_user.id][1] - 1]
        )

        # адрес места
        await message.answer(
            ADDRESSES[way_counter[message.from_user.id][0]][
                way_counter[message.from_user.id][1] - 1]
        )

        # как пройти
        await message.answer(
            HOW_TO_PASS[way_counter[message.from_user.id][0]][
                way_counter[message.from_user.id][1] - 1]
        )

        # Если текст подводка есть
        if INTRODUCTORY_TEXT[way_counter[message.from_user.id][0]][
                way_counter[message.from_user.id][1] - 1] != '':
            await message.answer(
                INTRODUCTORY_TEXT[way_counter[message.from_user.id][0]][
                    way_counter[message.from_user.id][1] - 1]
            )
            await message.answer(WRITE_YOUR_OPINION)
            # Ждём ввода текста
            await state.set_state(Cult_cuestions.question_1)
        # вариант, когда нет подводки
        else:
            await after_get_answer_1(message, state)
    else:
        # Поздравляем! Вы завершили маршрут.
        await message.answer(
            END_OF_WAY
        )

        # ссылка на форму обратной связи
        await message.answer(
            END_WAY_MESSAGE,
            reply_markup=keyboard_menu
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
    # отправка первой фотки экспоната
    await message.answer_photo(
        image_from_pc,
    )

    # отправление нескольких фоток экспонатов, если их нескольк
    # if (way_counter[message.from_user.id][0] == 1 and way_counter[message.from_user.id][1] == 1):
    #     await message.answer_photo(
    #         FSInputFile(
    #             os.path.join(dirname, 'pictures', '1', '1_1.jpg')
    #         ),
    #     )
    #     await message.answer_photo(
    #         FSInputFile(
    #             os.path.join(dirname, 'pictures', '1', '1_2.jpg')
    #         ),
    #     )
    #     await message.answer_photo(
    #         FSInputFile(
    #             os.path.join(dirname, 'pictures', '1', '1_3.jpg')
    #         ),
    #     )
    #
    # if (
    #     way_counter[message.from_user.id][0] == 3 and way_counter[message.from_user.id][1] == 2
    # ):
    #     await message.answer_photo(
    #         FSInputFile(
    #             os.path.join(dirname, 'pictures', '3', '2_1.jpg')
    #         ),
    #     )
    #
    # if (way_counter[message.from_user.id][0] == 3 and way_counter[message.from_user.id][1] == 10):
    #     await message.answer_photo(
    #         FSInputFile(
    #             os.path.join(dirname, 'pictures', '3', '10_1.jpg')
    #         ),
    #     )

    # текст экспоната
    await message.answer(TEXT_PLACE[way_counter[message.from_user.id][0]][way_counter[message.from_user.id][1] - 1])

    # вопрос для рефлексии
    if AFTER_QUESTION[way_counter[message.from_user.id][0]][
            way_counter[message.from_user.id][1] - 1] != '':
        await message.answer(AFTER_QUESTION[way_counter[message.from_user.id][0]][way_counter[message.from_user.id][1] - 1],)

    # ответ на рефлексию
    if AFTER_ANSWER[way_counter[message.from_user.id][0]][way_counter[message.from_user.id][1] - 1] != '':
        await message.answer(AFTER_ANSWER[way_counter[message.from_user.id][0]][way_counter[message.from_user.id][1] - 1])

    # Оценка работы
    await message.answer(RAITING_MESSAGE, reply_markup=keyboard_rating)

    # Ждём ввода текста
    await state.set_state(Cult_cuestions.raiting)

    # супер
    await message.answer(GREAT, reply_markup=keyboard_go_on_or_stop)
    return way_counter

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
async def what_can_do(message: Message):
    await message.answer(WHAT_I_CAN_DO, reply_markup=keyboard_menu)


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
        path = os.path.join(dirname, str(ex.image).replace('excursion/', ''))
        image_from_pc = FSInputFile(path)
        print(image_from_pc)
        print(path)
        await message.answer_photo(
            image_from_pc,
            caption=ex.name
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
    number_map = str(message.text).replace('/map ', '')
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
    ex = Route.objects.get(title=number_map)
    await message.answer(
        text=ex.description,
    )
    path = os.path.join(dirname, str(ex.route_map).replace('excursion/', ''))
    image_from_pc = FSInputFile(path)
    print(image_from_pc)
    print(path)
    await message.answer_photo(
        image_from_pc,
    )



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
async def do_audio(message: Message):
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
async def do_list(message: Message):
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
    user = message.from_user

    try:
        travel = Journey.objects.get(traveler=user.id)
        if travel.now_exhibit:
            ReviewOnExhibit(
                exhibit=Exhibit.objects.get(route=travel.route, order=travel.now_exhibit),
                author=user.username,
                contact=user.id,
                text=message.text
            ).save()

    except ObjectDoesNotExist:
        print("Объект не сушествует")
        return None
    except MultipleObjectsReturned:
        print("Найдено более одного объекта")
        return None

    await message.answer(
        text='спасибо!'
    )


