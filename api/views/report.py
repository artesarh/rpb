from rest_framework.routers import DefaultRouter
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from api.models import Report, ReportModifier
from api.serializers import (
    ReportSerializer,
    ReportWithModifierSerializer,
    EventGroupSerializer,
    LinkModifierRequestSerializer,
    LinkReportToModifierSerializer,
)
from drf_spectacular.utils import extend_schema, OpenApiResponse


class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.select_related("event_group").prefetch_related(
        "modifiers"
    )
    serializer_class = ReportSerializer

    def get_queryset(self):
        return self.queryset

    @action(detail=True, methods=["get"], url_path="modifiers/(?P<modifier_id>\d+)")
    def get_modifier(self, request, pk=None, modifier_id=None):
        report = self.get_object()
        modifier = get_object_or_404(
            ReportModifier, id=modifier_id, reports=report)
        serializer = ReportWithModifierSerializer(
            {"report": report, "modifier": modifier}, context={"request": request}
        )
        return Response(serializer.data)

    @action(detail=True, methods=["post"], url_path="link-modifier")
    @extend_schema(
        request=LinkModifierRequestSerializer,
        responses={
            200: OpenApiResponse(
                description="Successfully linked modifier",
                response=LinkReportToModifierSerializer,
            )
        },
    )
    def link_modifier(self, request, pk=None):
        serializer = LinkModifierRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        modifier_id = serializer.validated_data["modifier_id"]
        report = self.get_object()
        modifier = get_object_or_404(ReportModifier, id=modifier_id)
        report.modifiers.add(modifier)
        return Response(
            {"status": "success", "report_id": pk, "modifier_id": modifier_id}
        )

    @action(detail=True, methods=["get"], url_path="event-group")
    def get_event_group(self, request, pk=None):
        report = self.get_object()
        if not report.event_group:
            raise NotFound("No Event Group associated with this report")
        serializer = EventGroupSerializer(
            report.event_group, context={"request": request}
        )
        return Response(serializer.data)
