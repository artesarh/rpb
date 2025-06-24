from rest_framework import viewsets
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


class ReportModifierViewSet(viewsets.ModelViewSet):
    queryset = ReportModifier.objects.all()
    serializer_class = ReportModifierSerializer
    lookup_field = "id"  # The field on the model (usually 'id')
    lookup_url_kwarg = "modifier_id"  # The URL parameter name
    http_method_names = ["get", "post"]


class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    http_method_names = ["get", "post", "patch", "put"]


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    http_method_names = ["get", "delete"]


class EventGroupViewSet(viewsets.ModelViewSet):
    queryset = EventGroup.objects.all()
    serializer_class = EventGroupSerializer
    http_method_names = ["get", "post", "delete"]


class RingEventViewSet(viewsets.ModelViewSet):
    queryset = RingEvent.objects.all()
    serializer_class = RingEventSerializer
    http_method_names = ["get", "post", "delete"]


class BoxEventViewSet(viewsets.ModelViewSet):
    queryset = BoxEvent.objects.all()
    serializer_class = BoxEventSerializer
    http_method_names = ["get", "post", "delete"]


class GeoEventViewSet(viewsets.ModelViewSet):
    queryset = GeoEvent.objects.all()
    serializer_class = GeoEventSerializer
    http_method_names = ["get", "post", "delete"]
