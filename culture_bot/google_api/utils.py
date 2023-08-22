from datetime import datetime

from django.db.models import Avg
import pandas as pd
import plotly.express as px

from culture_bot import settings
from excursion.models import Exhibit, Route
from .models import ExhibitComment, RouteReview, UserFeedback


def create_user_feedback_and_route_review(
    telegram_id, selected_route_name, start_time
):
    route = Route.objects.get(title=selected_route_name)
    user_feedback = UserFeedback.objects.create(
        telegram_id=telegram_id,
        start_time_route=start_time,
        route_id=route.id
    )
    route_review = RouteReview.objects.create(
        user_id=user_feedback.id,
        route_id=route.id,
    )
    return route_review


def create_exhibit_comment(
    telegram_id, selected_route_name, exhibit_name, rating, text
):
    exhibit = Exhibit.objects.get(name=exhibit_name)
    route = Route.objects.get(name=selected_route_name)
    user_feedback = UserFeedback.objects.get(
        telegram_id=telegram_id, route_id=route.id
    )
    if text:
        user_feedback.exhibit_comment = True
        user_feedback.save()
    exhibit_comment = ExhibitComment.objects.create(
        user_feedback_id=user_feedback.id,
        route_id=route.id,
        exhibit_id=exhibit.id,
        rating_exhibit=rating,
        text=text
    )
    return exhibit_comment


def update_user_feedback_and_route_review(
    telegram_id, route_name, review_text, rating
):
    route = Route.objects.get(title=route_name)
    user_feedback = UserFeedback.objects.get(
        telegram_id=telegram_id, route_id=route.id
    )
    route_review = RouteReview.objects.get(
        user_feedback_id=user_feedback.id, route_id=route.id
    )
    user_feedback.end_time_route = datetime.now()
    if review_text:
        user_feedback.route_review = True
        route_review.text = review_text
    route_review.rating_route = rating
    user_feedback.save()
    route_review.save()
    return user_feedback, route_review


async def create_spreadsheet_body(data):
    now_date_time = datetime.now().strftime(settings.FORMAT)
    grid_properties = {
        'rowCount': settings.ROW_COUNT,
        'columnCount': settings.COLUMN_COUNT
    }
    
    route_sheets = [
        {
            'properties': {'title': title, 'gridProperties': grid_properties}
        } for title in data['for_routes_report']
    ]
    exhibit_sheets = [
        {
            'properties': {'title': title, 'gridProperties': grid_properties}
        } for title in data['for_exhibits_report']
    ]
    spreadsheet_body = {
        'properties': {
            'title': f'Отчет на {now_date_time}',
            'locale': 'ru_RU'
        },
        'sheets': [
            {
                'properties': {
                    'title': 'Общая статистика за все время',
                    'gridProperties': grid_properties
                }
            },
            {
                'properties': {
                    'title': 'Статистика по дням',
                    'gridProperties': grid_properties
                }
            },
            *route_sheets,
            *exhibit_sheets
        ]
    }
    return spreadsheet_body


def create_graph(data):
    rows = []
    for date, day_data in data['for_days_report'].items():
        visitors = day_data.get('visitors', 0)
        avg_ratings = {
            'Date': date, 'Общее количество пользователей': visitors
        }
        for route, route_data in data['for_routes_report'].items():
            total_rating = 0
            num_ratings = 0
            for rating_data in route_data:
                rating_date = rating_data['Data'][:10]
                if rating_date == date:
                    total_rating += rating_data['Rating']
                    num_ratings += 1
            if num_ratings > 0:
                avg_rating = total_rating / num_ratings
                avg_ratings[f'Средний рейтинг {route}'] = round(
                    avg_rating, 2
                )
            else:
                avg_ratings[f'Средний рейтинг {route}'] = None
        rows.append(avg_ratings)
    df = pd.DataFrame(rows)
    fig = px.line(df, x='Date', y=df.columns[1:], title='График по дням')
    fig.update_layout(
        xaxis_title='Date',
        yaxis_title='Количество поситителей и среднее значение рейтинга'
    )
    fig.update_layout(
        legend_title_text='Пользователи и рейтинг маршрутов'
    )
    return fig

def get_data_from_db(
    for_general_report=False,
    for_days_report=False,
    for_routes_report=False,
    for_exhibits_report=False
    ):
    data = {}
    data['for_general_report'] = {}
    data['for_days_report'] = {}
    data['for_routes_report'] = {}
    data['for_exhibits_report'] = {}
    if for_general_report:
        for route in Route.objects.all():
            data['for_general_report'][route.title] = {
                "Number_of_visitors": UserFeedback.objects.filter(
                    route=route.id).count(),
                "Average_rating": RouteReview.objects.filter(
                    route=route.id).aggregate(
                        Avg('rating_route'))['rating_route__avg'],
                "Number_of_route_reviews": RouteReview.objects.filter(
                    route=route.id).exclude(text='').count(),
                "Number_of_comments": ExhibitComment.objects.filter(
                    route=route.id).exclude(text='').count()
            }
    if for_days_report:
        for feedback in UserFeedback.objects.all():
            date = feedback.start_time_route.date().strftime('%Y-%m-%d')
            if date not in data['for_days_report']:
                data['for_days_report'][date] = {
                    "visitors": 0,
                    "reviews": 0,
                    "comments": 0
                }
            data['for_days_report'][date]['visitors'] += 1
            data['for_days_report'][date]['reviews'] = RouteReview.objects.filter(
                timestamp__date=date).exclude(text='').count()
            data['for_days_report'][date]['comments'] = ExhibitComment.objects.filter(
                timestamp__date=date).exclude(text='').count()
    if for_routes_report:
        for route in Route.objects.all():
            route_reviews = RouteReview.objects.filter(route=route.id)
            route_review_data = []
            for review in route_reviews:
                user_feedback = UserFeedback.objects.get(id=review.user_feedback_id)
                route_review_data.append({
                    "Telegram_ID": user_feedback.telegram_id,
                    "Rating": review.rating_route,
                    "Review": review.text,
                    "Data": review.timestamp.strftime('%Y-%m-%d %H:%M:%S')
                })
            data['for_routes_report'][route.title] = route_review_data
    if for_exhibits_report:
        for exhibit in Exhibit.objects.all():
            exhibit_comments = ExhibitComment.objects.filter(
                exhibit=exhibit.id
            )
            exhibit_data = []
            for comment in exhibit_comments:
                route_name = comment.exhibit.route.title
                user_feedback = UserFeedback.objects.get(
                    id=comment.user_feedback_id
                )
                exhibit_data.append({
                    "Name_route": route_name,
                    "Telegram_ID": user_feedback.telegram_id,
                    "Rating": comment.rating_exhibit,
                    "Comment": comment.text,
                    "Data": comment.timestamp.strftime('%Y-%m-%d %H:%M:%S')
                })
            data['for_exhibits_report'][exhibit.name] = exhibit_data
    return data


async def create_table_values(data, name, name_obj=None):
    now_date_time = datetime.now().strftime(settings.FORMAT)
    if name == 'for_general_report':
        table_values = [
            ['Отчет от', now_date_time],
            ['Общая статистика'],
            [
                'Название маршрута',
                'Количество посетителей',
                'Средняя оценка',
                'Количество отзывов маршрута',
                'Количество комментариев экспонатов'
            ]
        ]
        data_general = data['for_general_report']
        for key in data_general.keys():
            new_row = [
                key,
                data_general[key]['Number_of_visitors'],
                data_general[key]['Average_rating'],
                data_general[key]['Number_of_route_reviews'],
                data_general[key]['Number_of_comments']
            ]
            table_values.append(new_row)
        return table_values
    if name == 'for_days_report':
        table_values = [
            ['Отчет от', now_date_time],
            ['Статистика по дням'],
            [
                'День',
                'Количество посетителей',
                'Количество отзывов',
                'Количество комментариев',
            ]
        ]
        data_days = data['for_days_report']
        for key in data_days.keys():
            new_row = [
                key,
                data_days[key]['visitors'],
                data_days[key]['reviews'],
                data_days[key]['comments'],
            ]
            table_values.append(new_row)
        return table_values
    if name == 'for_routes_report':
        table_values = [
            ['Отчет от', now_date_time],
            ['Статистика по дням'],
            [
                'Маршрут',
                'Дата и время',
                'Рейтинг',
                'Телеграм id',
                'Отзыв'
            ]
        ]
        data_route = data['for_routes_report'][name_obj]
        for data_value in data_route:
            new_row = [
                name_obj,
                data_value['Data'],
                data_value['Rating'],
                data_value['Telegram_ID'],
                data_value['Review'],
            ]
            table_values.append(new_row)
        return table_values
    if name == 'for_exhibits_report':
        table_values = [
            ['Отчет от', now_date_time],
            ['Статистика по дням'],
            [
                'Экспонат',
                'Маршрут',
                'Дата и время',
                'Рейтинг',
                'Телеграм id',
                'Комментарий'
            ]
        ]
        data_exhibit = data['for_exhibits_report'][name_obj]
        for data_value in data_exhibit:
            new_row = [
                name_obj,
                data_value['Name_route'],
                data_value['Data'],
                data_value['Rating'],
                data_value['Telegram_ID'],
                data_value['Comment'],
            ]
            table_values.append(new_row)
        return table_values
