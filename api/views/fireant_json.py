from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from api.models.report import Report, ReportModifier
from api.models.event import Event, EventGroup
from api.serializers import (
    ReportSerializer,
    ReportWithModifiersSerializer,
    ReportWithEventGroupDetailSerializer,
    ReportWithEventGroupDetailModifierSerializer,
)


class FireantViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer

    @action(detail=True, methods=["get"], url_path="modifier/(?P<modifier_id>\d+)")
    def get_report_with_eventdetail_modifier(self, request, pk=None, modifier_id=None):
        report = self.get_object()
        eventgroup = report.event_group
        if not eventgroup:
            raise NotFound("No Event Group associated with report")

        modifier = report.modifiers.filter(id=modifier_id).first()

        if not modifier:
            raise NotFound("No modifier found")

        serializer = ReportWithEventGroupDetailModifierSerializer(
            {"report": report, "eventgroup": eventgroup, "modifier": modifier}
        )
        return Response(serializer.data)
