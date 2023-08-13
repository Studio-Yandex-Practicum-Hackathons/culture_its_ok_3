from datetime import datetime

from excursion.models import Route
from statistic.google_api import (
    set_user_permissions, spreadsheets_create, spreadsheets_update_value
)
from statistic.google_client import get_service
from statistic.models import UserFeedback, RouteReview, ExhibitComment


def create_user_feedback(telegram_id, start_time):
    user = UserFeedback.objects.create(
        telegram_id=telegram_id,
        start_time_route=start_time,
    )
    return user


def create_route_review(telegram_id, selected_route_name):
    user = UserFeedback.objects.get(telegram_id=telegram_id)
    route = Route.objects.get(title=selected_route_name)
    route_review = RouteReview.objects.create(
        user_id=user.id,
        route_id=route.id,
    )
    return route_review


def create_exhibit_comment(telegram_id, exhibit_name, rating, text):
    user = UserFeedback.objects.get(telegram_id=telegram_id)
    exhibit = Route.objects.get(name=exhibit_name)
    if text:
        user.exhibit_comment = True
        user.save()
    exhibit_comment = ExhibitComment.objects.create(
        user_id=user.id,
        exhibit_id=exhibit.id,
        rating_exhibit=rating,
        text=text
    )
    return exhibit_comment


def update_user_and_route_review(
    telegram_id, route_name, review_text, rating
):
    user = UserFeedback.objects.get(telegram_id=telegram_id)
    route = Route.objects.get(title=route_name)
    route_review = RouteReview.objects.get(user_id=user.id, route_id=route.id)
    user.end_time_route = datetime.now()
    if review_text:
        user.route_review = True
        route_review.text = review_text
    route_review.rating_route = rating
    user.save()
    route_review.save()
    return user, route_review


async def create_google_report(data, email):
    wrapper_services = get_service()
    spreadsheetid = await spreadsheets_create(wrapper_services)
    await set_user_permissions(spreadsheetid, wrapper_services, email)
    await spreadsheets_update_value(
        spreadsheetid,
        data,
        wrapper_services
    )
    return f'https://docs.google.com/spreadsheets/d/{spreadsheetid}'


def create_report():
    pass

def create_some_graph():
    pass
