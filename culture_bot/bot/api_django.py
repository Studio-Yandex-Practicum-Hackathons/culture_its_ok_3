import aiohttp
from datetime import datetime


async def create_userfeedback(telegram_id, route_id):
    async with aiohttp.ClientSession() as session:
        data = {
            'telegram_id': telegram_id,
            'route': route_id
        }
        async with session.post(
            'http://127.0.0.1:8000/api/user-feedback/', data=data
        ) as response:
            if response.status == 201:
                print("Запись о пользователе создана")
            else:
                print("Ошибка создания пользователя")

                
async def create_exhibit_comment_and_raiting(
    text, telegram_id, route_id, exhibit_name, rating_exhibit
    ):
    url = f"http://127.0.0.1:8000/api/user-feedback/get_by_telegram_id_and_route/"
    params = {
        'telegram_id': telegram_id,
        'route': route_id
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            if response.status == 200:
                feedback_data = await response.json()
                user_feedback_id = feedback_data.get('id')
                if user_feedback_id is not None:
                    url_comment = 'http://127.0.0.1:8000/api/exhibit-comment/'
                    params_comment = {
                        'text': text,
                        'user_feedback': user_feedback_id,
                        'route': route_id,
                        'exhibit': exhibit_name,
                        'rating_exhibit': rating_exhibit
                    }
                    async with session.post(
                        url_comment, json=params_comment
                    ) as update_response:
                        if update_response.status == 201:
                            print("Запись о рефлексии создана")
                        else:
                            print("Ошибка создания рефлексии")
                else:
                    print("Запись о пользователе не найдена")
            else:
                print("Ошибка получения данных о пользователе")


async def create_route_review_and_raiting(
    text, telegram_id, route_id, rating_route
    ):
    url = f"http://127.0.0.1:8000/api/user-feedback/get_by_telegram_id_and_route/"
    params = {
        'telegram_id': telegram_id,
        'route': route_id
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            if response.status == 200:
                feedback_data = await response.json()
                user_feedback_id = feedback_data.get('id')
                if user_feedback_id is not None:
                    url_comment = 'http://127.0.0.1:8000/api/route-review/'
                    params_comment = {
                        'text': text,
                        'user_feedback': user_feedback_id,
                        'route': route_id,
                        'rating_route': rating_route
                    }
                    async with session.post(
                        url_comment, json=params_comment
                    ) as update_response:
                        if update_response.status == 201:
                            print("Отзыв создан")
                        else:
                            print("Ошибка создания отзыва")
                else:
                    print("Запись о пользователе не найдена")
            else:
                print("Ошибка получения данных о пользователе")


async def update_userfeedback(telegram_id, route_id):
    url = f"http://127.0.0.1:8000/api/user-feedback/get_by_telegram_id_and_route/"
    params = {
        'telegram_id': telegram_id,
        'route': route_id
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            if response.status == 200:
                feedback_data = await response.json()
                user_feedback_id = feedback_data.get('id')
                if user_feedback_id is not None:
                    time_now = datetime.now().isoformat()
                    update_data = {
                        'end_time_route': time_now,
                    }
                    update_url = f'http://127.0.0.1:8000/api/user-feedback/{user_feedback_id}/'
                    async with session.patch(
                        update_url, json=update_data
                    ) as update_response:
                        if update_response.status == 200:
                            print("Запись о пользователе обновлена")
                        else:
                            print("Ошибка обновления пользователя")
                else:
                    print("Запись о пользователе не найдена")
            else:
                print("Ошибка получения данных о пользователе")
