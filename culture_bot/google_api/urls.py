from django.urls import include, path
from rest_framework.routers import DefaultRouter
from google_api.views import (
    UserFeedbackViewSet, ExhibitCommentViewSet, RouteReviewViewSet,
    RouteViewSet, ExhibitViewSet, CreateGoogleReportView
)

router = DefaultRouter()
router.register(r'user-feedback', UserFeedbackViewSet)
router.register(r'exhibit-comment', ExhibitCommentViewSet)
router.register(r'route-review', RouteReviewViewSet)
router.register(r'route', RouteViewSet)
router.register(r'exhibit', ExhibitViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('create-google-report/', CreateGoogleReportView.as_view(), name='create-google-report'),
]
