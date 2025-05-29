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


class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class EventGroupViewSet(viewsets.ModelViewSet):
    queryset = EventGroup.objects.all()
    serializer_class = EventGroupSerializer


class RingEventViewSet(viewsets.ModelViewSet):
    queryset = RingEvent.objects.all()
    serializer_class = RingEventSerializer


class BoxEventViewSet(viewsets.ModelViewSet):
    queryset = BoxEvent.objects.all()
    serializer_class = BoxEventSerializer


class GeoEventViewSet(viewsets.ModelViewSet):
    queryset = GeoEvent.objects.all()
    serializer_class = GeoEventSerializer
