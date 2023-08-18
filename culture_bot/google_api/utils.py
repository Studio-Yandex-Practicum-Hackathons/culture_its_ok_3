from datetime import datetime

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


def create_report():
    pass

def create_some_graph():
    pass
