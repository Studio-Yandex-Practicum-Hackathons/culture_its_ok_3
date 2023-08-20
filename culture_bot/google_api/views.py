import asyncio

from django.db.models import Avg
from rest_framework import status, viewsets
from rest_framework.response import Response

from excursion.models import Exhibit, Route
from .google_client import create_general_report
from google_api.models import ExhibitComment, RouteReview, UserFeedback
from google_api.serializers import (
    ExhibitCommentSerializer, ExhibitSerializer, RouteReviewSerializer,
    RouteSerializer, UserFeedbackSerializer
)

# for statistics and google sheets

class CreateGoogleGeneralReportViewSet(viewsets.ViewSet):

    def list(self, request):
        data = {}
        data['for_general_report'] = {}
        data['for_days_report'] = {}
        data['for_routes_report'] = {}
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
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        results = loop.run_until_complete(create_general_report(data))
        return Response({"result": results}, status=status.HTTP_200_OK)

# for test views create

class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer


class ExhibitViewSet(viewsets.ModelViewSet):
    queryset = Exhibit.objects.all()
    serializer_class = ExhibitSerializer


class UserFeedbackViewSet(viewsets.ModelViewSet):
    queryset = UserFeedback.objects.all()
    serializer_class = UserFeedbackSerializer


class ExhibitCommentViewSet(viewsets.ModelViewSet):
    queryset = ExhibitComment.objects.all()
    serializer_class = ExhibitCommentSerializer


class RouteReviewViewSet(viewsets.ModelViewSet):
    queryset = RouteReview.objects.all()
    serializer_class = RouteReviewSerializer

