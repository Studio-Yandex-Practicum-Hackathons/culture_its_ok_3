from datetime import datetime

import plotly.graph_objects as go

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
            *route_sheets
        ]
    }
    return spreadsheet_body


def create_graph(data):
    fig = go.Figure()
    dates = list(data['for_graph'].keys())
    visitors = [item['visitors'] for item in data['for_graph'].values()]
    reviews = [item['reviews'] for item in data['for_graph'].values()]
    comments = [item['comments'] for item in data['for_graph'].values()]
    fig.add_trace(go.Scatter(
        x=dates, y=visitors, mode='lines+markers', name='Посетители'))
    fig.add_trace(go.Scatter(
        x=dates, y=reviews, mode='lines+markers', name='Отзывы'))
    fig.add_trace(go.Scatter(
        x=dates, y=comments, mode='lines+markers', name='Комментарии'))
    graph_html = fig.to_html(full_html=False, default_height=300)
    return graph_html


async def create_table_values(data, name, name_route=None):
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
        data_route = data['for_routes_report'][name_route]
        for data_value in data_route:
            new_row = [
                name_route,
                data_value['Data'],
                data_value['Rating'],
                data_value['Telegram_ID'],
                data_value['Review'],
            ]
            table_values.append(new_row)
    return table_values
