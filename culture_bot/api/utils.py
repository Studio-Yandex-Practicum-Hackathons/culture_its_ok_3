from django.db.models import Avg
import pandas as pd
import plotly.express as px

from excursion.models import Exhibit, Route
from google_api.models import ExhibitComment, RouteReview, UserFeedback


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
                user_feedback = UserFeedback.objects.get(
                    id=review.user_feedback_id
                )
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
