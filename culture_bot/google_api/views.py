import asyncio

from django.db.models import Avg
from rest_framework import status, viewsets
from rest_framework.response import Response

from excursion.models import Exhibit, Route
from .google_client import create_report
from google_api.models import ExhibitComment, RouteReview, UserFeedback
from google_api.serializers import (
    ExhibitCommentSerializer, ExhibitSerializer, RouteReviewSerializer,
    RouteSerializer, UserFeedbackSerializer
)

# for statistics and google sheets

class CreateGoogleGeneralReportViewSet(viewsets.ViewSet):

    def list(self, request):
        data = {}
        routes = Route.objects.all()
        for route in routes:
            number_of_visitors = UserFeedback.objects.filter(
                route=route.id).count()
            average_rating = RouteReview.objects.filter(
                route=route.id).aggregate(
                    Avg('rating_route'))['rating_route__avg']
            number_of_route_reviews = RouteReview.objects.filter(
                route=route.id).exclude(text='').count()
            number_of_comments_on_exhibits = ExhibitComment.objects.filter(
                route=route.id).exclude(text='').count()
            data.update({
                route.title: {
                    "Number_of_visitors": number_of_visitors,
                    "Average_rating": average_rating,
                    "Number_of_route_reviews": number_of_route_reviews,
                    "Number_of_comments": number_of_comments_on_exhibits
                }
            })
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        results = loop.run_until_complete(create_report(data))
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

