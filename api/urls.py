# api/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from api.views import (
    ReportViewSet,
    ReportModifierViewSet,
    JobViewSet,
    EventViewSet,
    EventGroupViewSet,
    RingEventViewSet,
    BoxEventViewSet,
    GeoEventViewSet,
)


router = DefaultRouter()
router.register(r"reports", ReportViewSet, basename="report")
router.register(r"report-modifiers", ReportModifierViewSet, basename="report-modifier")
router.register(r"jobs", JobViewSet, basename="job")
router.register(r"events", EventViewSet, basename="event")
router.register(r"event-groups", EventGroupViewSet, basename="event-group")
router.register(r"ring-events", RingEventViewSet, basename="ring-event")
router.register(r"box-events", BoxEventViewSet, basename="box-event")
router.register(r"geo-events", GeoEventViewSet, basename="geo-event")

app_name = "api"  # Ensure namespace is defined

urlpatterns = [
    path("", include(router.urls), name="api-root"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path(
        "docs/", SpectacularSwaggerView.as_view(url_name="api:schema"), name="swagger"
    ),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "docs/redoc/", SpectacularRedocView.as_view(url_name="api:schema"), name="redoc"
    ),
]
