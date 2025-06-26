from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from api.models.report import ReportModifier
from api.models.job import Job
from api.models.event import Event, EventGroup, RingEvent, BoxEvent, GeoEvent
from api.serializers import (
    ReportModifierSerializer,
    JobSerializer,
    EventSerializer,
    EventGroupSerializer,
    RingEventSerializer,
    BoxEventSerializer,
    GeoEventSerializer,
)


class StandardResultsPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response(
            {
                "meta": {
                    "pagination": {
                        "page": self.page.number,
                        "pages": self.page.paginator.num_pages,
                        "per_page": self.page_size,
                        "total": self.page.paginator.count,
                        "has_next": self.page.has_next(),
                        "has_previous": self.page.has_previous(),
                    }
                },
                "links": {
                    "next": self.get_next_link(),
                    "previous": self.get_previous_link(),
                },
                "data": data,
            }
        )


class BaseViewSetMixin:
    """Base mixin that provides common functionality for all viewsets"""

    pagination_class = StandardResultsPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    @action(detail=False, methods=["get"])
    def metadata(self, request):
        """Provide metadata about the resource"""
        # Get the queryset through the method to handle dynamic querysets
        queryset = (
            self.get_queryset()
            if hasattr(self, "get_queryset")
            else getattr(self, "queryset", None)
        )
        model = queryset.model if queryset else None

        response_data = {
            "actions": {
                "list": f"{request.build_absolute_uri()}",
                "create": f"{request.build_absolute_uri()}",
                "detail": f"{request.build_absolute_uri()}{{id}}/",
                "update": f"{request.build_absolute_uri()}{{id}}/",
                "delete": f"{request.build_absolute_uri()}{{id}}/",
            },
            "filters": getattr(self, "filterset_fields", []),
            "search_fields": getattr(self, "search_fields", []),
            "ordering_fields": getattr(self, "ordering_fields", []),
        }

        if model:
            response_data.update(
                {
                    "model": model.__name__,
                    "fields": [field.name for field in model._meta.fields],
                }
            )

        return Response(response_data)


class ReportModifierViewSet(BaseViewSetMixin, viewsets.ModelViewSet):
    queryset = ReportModifier.objects.all()
    serializer_class = ReportModifierSerializer
    lookup_field = "id"
    lookup_url_kwarg = "modifier_id"
    http_method_names = ["get", "post"]

    # Enhanced filtering and search
    filterset_fields = ["as_at_date", "fx_date"]
    search_fields = ["as_at_date"]
    ordering_fields = ["as_at_date", "fx_date", "id"]
    ordering = ["-as_at_date"]

    @action(detail=True, methods=["get"])
    def reports(self, request, modifier_id=None):
        """Get all reports associated with this modifier"""
        modifier = self.get_object()
        reports = modifier.reports.all()

        # Import here to avoid circular imports
        from api.serializers.report import ReportSerializer

        serializer = ReportSerializer(reports, many=True, context={"request": request})

        return Response(
            {
                "meta": {"modifier_id": modifier.id, "reports_count": reports.count()},
                "data": serializer.data,
            }
        )


class JobViewSet(BaseViewSetMixin, viewsets.ModelViewSet):
    queryset = Job.objects.select_related("report", "report_modifier")
    serializer_class = JobSerializer
    http_method_names = ["get", "post", "patch"]

    filterset_fields = ["report", "report_modifier", "fireant_jobid"]
    search_fields = ["fireant_jobid", "report__name"]
    ordering_fields = ["created", "updated", "fireant_jobid"]
    ordering = ["-created"]


class EventViewSet(BaseViewSetMixin, viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    http_method_names = ["get"]

    filterset_fields = ["is_valid", "zone"]
    search_fields = ["name", "description", "zone"]
    ordering_fields = ["name", "zone", "id"]
    ordering = ["name"]

    @action(detail=True, methods=["get"])
    def event_groups(self, request, pk=None):
        """Get all event groups that contain this event"""
        event = self.get_object()
        groups = event.event_groups.all()
        serializer = EventGroupSerializer(
            groups, many=True, context={"request": request}
        )

        return Response(
            {
                "meta": {"event_id": event.id, "groups_count": groups.count()},
                "data": serializer.data,
            }
        )


class EventGroupViewSet(BaseViewSetMixin, viewsets.ModelViewSet):
    queryset = EventGroup.objects.prefetch_related("events")
    serializer_class = EventGroupSerializer
    http_method_names = ["get", "post", "patch", "delete"]

    search_fields = ["name"]
    ordering_fields = ["name", "created", "updated"]
    ordering = ["-created"]

    @action(detail=True, methods=["get"])
    def reports(self, request, pk=None):
        """Get all reports that use this event group"""
        event_group = self.get_object()
        reports = event_group.reports.all()

        # Import here to avoid circular imports
        from api.serializers.report import ReportSerializer

        serializer = ReportSerializer(reports, many=True, context={"request": request})

        return Response(
            {
                "meta": {
                    "event_group_id": event_group.id,
                    "reports_count": reports.count(),
                },
                "data": serializer.data,
            }
        )


class RingEventViewSet(BaseViewSetMixin, viewsets.ModelViewSet):
    queryset = RingEvent.objects.all()
    serializer_class = RingEventSerializer
    http_method_names = ["get", "post", "patch", "delete"]

    filterset_fields = ["is_valid", "zone"]
    search_fields = ["name", "description", "zone"]
    ordering_fields = ["name", "latitude", "longitude", "radius"]
    ordering = ["name"]


class BoxEventViewSet(BaseViewSetMixin, viewsets.ModelViewSet):
    queryset = BoxEvent.objects.all()
    serializer_class = BoxEventSerializer
    http_method_names = ["get", "post", "patch", "delete"]

    filterset_fields = ["is_valid", "zone"]
    search_fields = ["name", "description", "zone"]
    ordering_fields = ["name", "max_lat", "min_lat", "max_lon", "min_lon"]
    ordering = ["name"]


class GeoEventViewSet(BaseViewSetMixin, viewsets.ModelViewSet):
    queryset = GeoEvent.objects.all()
    serializer_class = GeoEventSerializer
    http_method_names = ["get", "post", "patch", "delete"]

    filterset_fields = ["is_valid", "country", "area", "subarea"]
    search_fields = ["name", "description", "country", "area", "subarea"]
    ordering_fields = ["name", "country", "area"]
    ordering = ["country", "name"]
