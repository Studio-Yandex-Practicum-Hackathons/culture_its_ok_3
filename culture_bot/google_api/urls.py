from django.urls import include, path
from rest_framework.routers import DefaultRouter

from google_api.views import (
    CreateGoogleGeneralReportViewSet, ExhibitCommentViewSet, ExhibitViewSet,
    RouteReviewViewSet, RouteViewSet, UserFeedbackViewSet
)

router = DefaultRouter()
router.register(r'user-feedback', UserFeedbackViewSet)
router.register(r'exhibit-comment', ExhibitCommentViewSet)
router.register(r'route-review', RouteReviewViewSet)
router.register(r'route', RouteViewSet)
router.register(r'exhibit', ExhibitViewSet)
router.register(
    r'create-google-report',
    CreateGoogleGeneralReportViewSet,
    base_name='create-google-report'
)

urlpatterns = [
    path('', include(router.urls)),
]
