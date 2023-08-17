import asyncio

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from google_api.models import UserFeedback, ExhibitComment, RouteReview
from google_api.serializers import (
    UserFeedbackSerializer, ExhibitCommentSerializer, RouteReviewSerializer,
    RouteSerializer, ExhibitSerializer
)
from excursion.models import Route, Exhibit

from .google_client import create_report

# for statistics and google sheets


class CreateGoogleReportView(APIView):

    def post(self, request, *args, **kwargs):
        user_feedbacks = UserFeedback.objects.all()
        exhibit_comments = ExhibitComment.objects.all()
        route_reviews = RouteReview.objects.all()
        all_data = [user_feedbacks, exhibit_comments, route_reviews]
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        results = loop.run_until_complete(create_report(all_data))
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

