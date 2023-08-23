from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (
    CreateGoogleGeneralReportViewSet, ExhibitCommentViewSet, ExhibitViewSet,
    GraphViewSet, RouteReviewViewSet, RouteViewSet, UserFeedbackViewSet,
)

router = DefaultRouter()
router.register(r'user-feedback', UserFeedbackViewSet, basename='user-feedback')
router.register(r'exhibit-comment', ExhibitCommentViewSet)
router.register(r'route-review', RouteReviewViewSet)
router.register(r'route', RouteViewSet)
router.register(r'exhibit', ExhibitViewSet)
router.register(
    r'create-google-report',
    CreateGoogleGeneralReportViewSet,
    base_name='create-google-report'
)
router.register(r'create-graph', GraphViewSet, basename='graph')

urlpatterns = [
    path('', include(router.urls)),
]
