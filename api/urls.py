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
    LinkModifierViewSet,
    api_root,
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
router.register(r"link-modifier", LinkModifierViewSet, basename="link-modifier")
app_name = "api"  # Ensure namespace is defined

urlpatterns = [
    path("", api_root, name="api-root"),
    path("", include(router.urls)),
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
