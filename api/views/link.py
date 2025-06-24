from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, OpenApiResponse
from api.serializers import (
    LinkMultipleReportsToModifiersIn,
    LinkMultipleReportsToModifiersOut,
    LinkReportToModifierSerializerIn,
    LinkReportToModifierSerializerOut,
)


class LinkModifierViewSet(ViewSet):
    @extend_schema(
        request=LinkReportToModifierSerializerIn,
        responses={
            200: LinkReportToModifierSerializerOut,
            400: OpenApiResponse(description="Invalid input"),
            404: OpenApiResponse(description="Report or modifier not found"),
        },
        operation_id="link_single_report_modifier",
    )
    @action(detail=False, methods=["post"], url_path="single")
    def single(self, request):
        serializer = LinkReportToModifierSerializerIn(data=request.data)
        serializer.is_valid(raise_exception=True)
        modifier_id = serializer.validated_data["modifier_id"]
        report_id = serializer.validated_data["report_id"]

        report = get_object_or_404(Report, id=report_id)
        modifier = get_object_or_404(ReportModifier, id=modifier_id)
        report.modifiers.add(modifier)

        return Response(
            LinkReportToModifierSerializerOut(
                {
                    "status": "success",
                    "report_id": report_id,
                    "modifier_id": modifier_id,
                }
            ).data,
            status=200,
        )

    @extend_schema(
        request=LinkMultipleReportsToModifiersIn,
        responses={
            200: LinkMultipleReportsToModifiersOut,
            400: OpenApiResponse(description="Invalid input"),
            404: OpenApiResponse(description="Report or modifier not found"),
        },
        operation_id="link_multiple_reports_modifiers",
    )
    @action(detail=False, methods=["post"], url_path="multiple")
    def multiple(self, request):
        serializer = LinkMultipleReportsToModifiersIn(data=request.data)
        serializer.is_valid(raise_exception=True)

        reports = serializer.validated_data["reports"]
        modifiers = serializer.validated_data["modifiers"]

        for r in reports:
            for m in modifiers:
                this_report = get_object_or_404(Report, id=r)
                this_modifier = get_object_or_404(ReportModifier, id=m)
                this_report.modifiers.add(this_modifier)

        return Response(
            LinkMultipleReportsToModifiersOut(
                {
                    "status": "success",
                    "reports": reports,
                    "modifiers": modifiers,
                }
            ).data,
            status=200,
        )
