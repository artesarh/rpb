from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse
from api.models import Report, ReportModifier
from api.serializers import (
    ReportSerializer,
    ReportModifierSerializer,
    ReportWithAllSerializer,
    ReportWithModifierSerializer,
    ReportWithModifiersListSerializer,
    EventGroupSerializer,
)


class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.select_related("event_group").prefetch_related(
        "modifiers"
    )
    serializer_class = ReportSerializer
    http_method_names = ["get", "post", "patch", "put"]

    def get_queryset(self):
        return self.queryset

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="modifier_id",
                type=int,
                location=OpenApiParameter.PATH,
                description="ID of the modifier to retrieve",
            )
        ],
        responses={
            200: ReportWithModifierSerializer,
            404: OpenApiResponse(description="Report or modifier not found"),
        },
        operation_id="get_report_modifier",
    )
    @action(detail=True, methods=["get"], url_path="modifiers/(?P<modifier_id>\d+)")
    def get_modifier(self, request, pk=None, modifier_id=None):
        """Get a specific report and a specific modifier."""
        report = self.get_object()
        modifier = get_object_or_404(ReportModifier, id=modifier_id, reports=report)
        serializer = ReportWithModifierSerializer(
            {"report": report, "modifier": modifier}, context={"request": request}
        )
        return Response(serializer.data)

    @extend_schema(
        responses={
            200: ReportWithModifiersListSerializer,
            404: OpenApiResponse(description="Report or modifiers not found"),
        },
        operation_id="get_report_modifiers_list",
    )
    @action(detail=True, methods=["get"], url_path="modifiers")
    def get_modifiers_list(self, request, pk=None):
        """Get a report with all its modifiers."""

        report = self.get_object()
        modifiers = ReportModifier.objects.filter(reports=report)
        if not modifiers.exists():
            raise NotFound("No modifiers found for this report.")
        serializer = ReportWithModifiersListSerializer(
            {"report": report, "modifiers": modifiers}, context={"request": request}
        )
        return Response(serializer.data)

    @extend_schema(
        responses={
            200: ReportWithAllSerializer,
            404: OpenApiResponse(description="Report or modifiers not found"),
        },
        operation_id="get_report_modifiers_list",
    )
    @action(detail=True, methods=["get"], url_path="modifier/(?P<modifier_id>\d+)/all")
    def get_report_with_eventdetail_modifier(self, request, pk=None, modifier_id=None):
        report = self.get_object()
        eventgroup = report.event_group
        if not eventgroup:
            raise NotFound("No Event Group associated with report")

        modifier = report.modifiers.filter(id=modifier_id).first()

        if not modifier:
            raise NotFound("No modifier found")

        serializer = ReportWithAllSerializer(
            {"report": report, "eventgroup": eventgroup, "modifier": modifier}
        )
        return Response(serializer.data)
