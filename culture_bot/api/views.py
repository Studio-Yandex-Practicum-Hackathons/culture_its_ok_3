import asyncio

from rest_framework import status, viewsets
from rest_framework.response import Response
from api.utils import get_data_from_db
from google_api.google_client import create_general_report


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
