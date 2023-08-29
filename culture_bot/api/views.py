import asyncio

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from api.serializers import (ExhibitCommentSerializer, ExhibitSerializer,
                             RouteReviewSerializer, RouteSerializer,
                             UserFeedbackSerializer)
from api.utils import get_data_from_db
from excursion.models import Exhibit, Route
from google_api.google_client import create_general_report
from google_api.models import ExhibitComment, RouteReview, UserFeedback


class UserFeedbackViewSet(viewsets.ModelViewSet):
    queryset = UserFeedback.objects.all()
    serializer_class = UserFeedbackSerializer

    def create(self, request):
        serializer = UserFeedbackSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User feedback created successfully"},
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=['get'])
    def get_by_telegram_id_and_route(self, request):
        telegram_id = request.query_params.get('telegram_id')
        route = request.query_params.get('route')
        try:
            user_feedback = UserFeedback.objects.get(
                telegram_id=telegram_id, route=route
            )
            serializer = self.serializer_class(user_feedback)
            return Response(serializer.data)
        except UserFeedback.DoesNotExist:
            return Response(
                {"message": "User feedback not found"},
                status=status.HTTP_404_NOT_FOUND
            )


class ExhibitCommentViewSet(viewsets.ModelViewSet):
    queryset = ExhibitComment.objects.all()
    serializer_class = ExhibitCommentSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateGoogleGeneralReportViewSet(viewsets.ViewSet):

    def list(self, request):
        data = get_data_from_db(
        for_general_report=True,
        for_days_report=True,
        for_routes_report=True,
        for_exhibits_report=True
        )
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        results = loop.run_until_complete(create_general_report(data))
        return Response({"result": results}, status=status.HTTP_200_OK)


class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer


class ExhibitViewSet(viewsets.ModelViewSet):
    queryset = Exhibit.objects.all()
    serializer_class = ExhibitSerializer


class RouteReviewViewSet(viewsets.ModelViewSet):
    queryset = RouteReview.objects.all()
    serializer_class = RouteReviewSerializer
