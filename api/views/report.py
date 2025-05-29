from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from api.models.report import Report, ReportModifier
from api.models.event import Event, EventGroup
from api.serializers import (
    ReportSerializer,
    ReportWithModifierSerializer,
    ReportWithEventGroupDetailSerializer,
    ReportWithEventGroupDetailModifierSerializer,
)


class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer

    @action(detail=True, methods=["get"], url_path="modifier/(?P<modifier_id>\d+)")
    def get_report_with_specific_modifier(self, request, pk=None, modifier_id=None):
        report = self.get_object()
        try:
            modifier = ReportModifier.objects.get(id=modifier_id, reports=report)
        except ReportModifier.DoesNotExist:
            raise NotFound(
                "ReportModifier not found or not associated with this report."
            )
        serializer = ReportWithModifierSerializer(
            {"report": report, "modifier": modifier}
        )
        return Response(serializer.data)

    @action(detail=True, methods=["get"], url_path="link-modifier/(?P<modifier_id>\d+)")
    def link_report_with_modifier(self, request, pk=None, modifier_id=None):
        report = self.get_object()
        try:
            modifier = ReportModifier.objects.get(id=modifier_id)
            report.modifiers.add(modifier)
        except ReportModifier.DoesNotExist:
            raise NotFound("Report modifier not found")

        except Report.DoesNotExist:
            raise NotFound("Report does not exist")

        return Response("Success")

    @action(detail=True, methods=["get"], url_path="events")
    def get_report_with_eventgroup_detail(self, request, pk=None):
        report = self.get_object()
        eventgroup = report.event_group
        if not eventgroup:
            raise NotFound("No Event Group associated with this report")

        serializer = ReportWithEventGroupDetailSerializer(
            {"report": report, "eventgroup": eventgroup}, context={"request": request}
        )
        return Response(serializer.data)

    @action(
        detail=True, methods=["get"], url_path="modifier/(?P<modifier_id>\d+)/events"
    )
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
