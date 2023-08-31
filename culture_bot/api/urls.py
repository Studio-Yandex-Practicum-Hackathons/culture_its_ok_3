from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import CreateGoogleGeneralReportViewSet

router = DefaultRouter()
router.register(
    r'create-google-report',
    CreateGoogleGeneralReportViewSet,
    base_name='create-google-report'
)

urlpatterns = [
    path('', include(router.urls)),
]
