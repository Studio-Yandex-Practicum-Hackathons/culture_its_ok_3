import os
import sys

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import FSInputFile, Message
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.utils import timezone
from dotenv import load_dotenv

from google_api.models import ExhibitComment, RouteReview, UserFeedback

from .custom_keyboard import *
from .messages import *
from .models import Exhibit, Journey, ReflectionExhibit, Route

load_dotenv()

dirname = os.path.dirname(__file__)

router = Router()


class Cult_cuestions(StatesGroup):
    question_1 = State()
    raiting = State()
    review_text = State()
    route_rating = State()


@router.message(Command('start'))
@router.message(F.text == 'Меню')
async def start_bot(message: Message):
    await message.answer(
        START_MESSAGE,
        reply_markup=keyboard_ways
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


@router.message(F.text == 'Завершить медитацию')
@router.message(Command('end'))
async def stop_journey(message: Message):
    Journey.objects.get(traveler=message.from_user.id).delete()
    await message.answer(STOP_JOURNY, reply_markup=keyboard_menu)


@router.message(F.text == 'О проекте')
async def about(message: Message):
    await message.answer(ABOUT, reply_markup=keyboard_menu)


@router.message(F.text == 'Что ты умеешь?')
async def what_i_an_do(message: Message):
    await message.answer(WHAT_I_CAN_DO, reply_markup=keyboard_menu)


@router.message(F.text == 'Я готов')
@router.message(Command('next'))
async def go_next_exhibit(message: Message):
    chat_id = message.from_user.id

    tr = Journey.objects.get(traveler=chat_id)
    count_exhibit_on_rout = Route.objects.get(title=tr.route.title).exhibit.count()
    print(count_exhibit_on_rout)
    print(tr.now_exhibit)
    if tr.now_exhibit < count_exhibit_on_rout:
        ex = Exhibit.objects.get(route__title=tr.route, order=tr.now_exhibit + 1)

        tr.now_exhibit = tr.now_exhibit + 1
        tr.save()

        await message.answer(text=ex.name)
        await message.answer(text=f'Художник {ex.name}')
        await message.answer(text=ex.address)
        await message.answer(text=f'как пройти:\n{ex.where_start}')

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

        question_for_reflection = ex.question_for_reflection or None
        if question_for_reflection:
            await message.answer(text=question_for_reflection)

    elif tr.now_exhibit == count_exhibit_on_rout:
        tr.now_exhibit = tr.now_exhibit + 1
        await processing_free_content(message)


# если находимся не рядом с местом медитации
async def not_start_place(message: Message):
    chat_id = message.from_user.id

    tr = Journey.objects.get(traveler=chat_id)
    await message.answer(MEDITATION_ADRESS)
    await message.answer(tr.route.where_start)
    await message.answer(NOT_START_PLACE)
    await message.answer(START_WAY_QUESTION, reply_markup=keyboard_only_ready)


#  выбор маршрута
async def route_selection(message: Message):
    chat_id = message.from_user.id

    number_map = str(message.text)

    Journey.objects.filter(traveler=chat_id).delete()
    route = Route.objects.get(title=number_map)
    Journey(
        traveler=chat_id,
        route=route,
        now_exhibit=0
    ).save()

    UserFeedback(
        telegram_id=chat_id,
        route=route
    ).save()

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
    await message.answer(START_WAY_QUESTION, reply_markup=keyboard_ready)

    return None


async def processing_free_content(message: Message):
    user = message.from_user

    try:

        travel = Journey.objects.get(traveler=user.id)
        count_exhibit_on_rout = Route.objects.get(title=travel.route.title).exhibit.count()

        if travel.now_exhibit <= count_exhibit_on_rout:
            ReflectionExhibit(
                exhibit=Exhibit.objects.get(route=travel.route, order=travel.now_exhibit),
                author=user.username,
                contact=user.id,
                text=message.text,
                rating=1
            ).save()
            ExhibitComment(
                text=message.text,
                user_feedback=list(UserFeedback.objects.filter(telegram_id=user.id, route=travel.route))[-1],
                exhibit=Exhibit.objects.get(route=travel.route, order=travel.now_exhibit),
                route=travel.route
            ).save()
        elif travel.now_exhibit > count_exhibit_on_rout:
            RouteReview(
                text=message.text,
                user_feedback=list(UserFeedback.objects.filter(telegram_id=user.id, route=travel.route))[-1],
                route=travel.route
            ).save()

        # ответ на рефлексию
        answer = Exhibit.objects.get(route=travel.route, order=travel.now_exhibit).answer_for_reflection or None
        if answer:
            await message.answer(text=answer)

    except ObjectDoesNotExist:
        print('Объект не сушествует')
        await start_bot(message)
        return None
    except MultipleObjectsReturned:
        print('Найдено более одного объекта')
        await start_bot(message)
        return None

    await message.answer(text=RESPONSE_REFLECTION[randint(0, len(RESPONSE_REFLECTION)-1)])
    await message.answer(RAITING_MESSAGE, reply_markup=keyboard_rating)

    return None


async def set_rating_exhibit(message: Message, state: FSMContext):
    user = message.from_user
    try:
        num = int(message.text)
        travel = Journey.objects.get(traveler=user.id)
        count_exhibit_on_rout = Route.objects.get(title=travel.route.title).exhibit.count()
        if travel.now_exhibit > count_exhibit_on_rout:
            review_rout = list(RouteReview.objects.filter(
                user_feedback=list(UserFeedback.objects.filter(telegram_id=user.id, route=travel.route))[-1],
                route=travel.route
            ))[-1]
            review_rout.rating_route = num
            review_rout.save()
            return None
        else:
            refl = list(ReflectionExhibit.objects.filter(
                exhibit=Exhibit.objects.get(route=travel.route, order=travel.now_exhibit),
                author=user.username,
                contact=user.id))[-1]

            comment = list(ExhibitComment.objects.filter(
                user_feedback=list(UserFeedback.objects.filter(telegram_id=user.id, route=travel.route))[-1],
                exhibit=list(Exhibit.objects.filter(route=travel.route, order=travel.now_exhibit))[-1],
                route=travel.route))[-1]
            refl.rating = num
            comment.rating_exhibit = num
            comment.save()
            refl.save()
            if travel.now_exhibit == count_exhibit_on_rout:
                travel.now_exhibit += 1

        if 1 <= num < 4:
            await message.answer(text='Это нормально, что вам что-то не понравилось, спасибо за отзыв')
        elif 4 <= num < 7:
            await message.answer(text='Приятно видеть от вас такую оценку')
        else:
            await message.answer(text='Большое спасибо! Мы передадим вашу оценку автору :)')

        if travel.now_exhibit > count_exhibit_on_rout:
            await message.answer(
                END_OF_WAY
            )

            # ссылка на форму обратной связи
            # await message.answer(
            #     END_WAY_MESSAGE,
            #     reply_markup=keyboard_menu
            # )

            # другая концовка с вводом отзыва и рейтинга
            await message.answer(END_WAY_MESSAGE_2)
            await state.set_state(Cult_cuestions.review_text)
            return None

        await message.answer(GREAT, reply_markup=keyboard_go_on_or_stop)

    except ObjectDoesNotExist:
        print('Объект не сушествует')
        return None
    except MultipleObjectsReturned:
        print('Найдено более одного объекта')
        return None


@router.message(F.text)
async def handle_message(message: Message, state: FSMContext):
    current_state = await state.get_state()
    routs_all = [rout.title for rout in Route.objects.all()]
    message_text = message.text
    if current_state == Cult_cuestions.review_text:
        await after_get_review_message(message, state)
        return None
    elif current_state == Cult_cuestions.route_rating:
        await after_get_route_rating(message, state)
        return None
    elif message_text in routs_all:
        await route_selection(message)
        return None

    elif message_text.isdigit():
        await set_rating_exhibit(message, state)
        return None

    elif message_text in SEARCH_FOR_PLACE:
        await not_start_place(message)
        return None

    elif message_text in LET_MOVE_ON:
        await go_next_exhibit(message)
        return None

    else:
        await processing_free_content(message)
        return None


@router.message(Cult_cuestions.review_text)
async def after_get_review_message(message: Message, state: FSMContext):
    if message.text:
        await state.update_data(review_text=message.text)
    await state.set_state(Cult_cuestions.route_rating)
    await message.answer(REVIEW_THANKS)
    await message.answer(
        RAITING_REVIEW,
        reply_markup=keyboard_rating
    )
    await state.set_state(Cult_cuestions.route_rating)


@router.message(Cult_cuestions.route_rating)
async def after_get_route_rating(message: Message, state: FSMContext):
    current_time = timezone.now()
    user = message.from_user
    travel = Journey.objects.get(traveler=user.id)
    data = await state.get_data()
    review_text = data.get('review_text', '')
    RouteReview(
        text=review_text,
        user_feedback=list(UserFeedback.objects.filter(
            telegram_id=user.id, route=travel.route
        ))[-1],
        route=travel.route,
        rating_route=int(message.text)
    ).save()
    user_feedback=list(UserFeedback.objects.filter(
        telegram_id=user.id, route=travel.route
    ))[-1]
    user_feedback.end_time_route = current_time
    user_feedback.save()
    await message.answer(
        RAITING_THANKS,
        reply_markup=keyboard_menu
    )
    travel.delete()
