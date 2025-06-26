from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db import transaction
from drf_spectacular.utils import extend_schema, OpenApiResponse
from api.serializers import (
    LinkMultipleReportsToModifiersIn,
    LinkMultipleReportsToModifiersOut,
    LinkReportToModifierSerializerIn,
    LinkReportToModifierSerializerOut,
)
from api.models import (
    Report,
    ReportModifier,
)


class LinkModifierViewSet(ViewSet):
    """
    ViewSet for managing relationships between Reports and ReportModifiers.
    
    This provides operations to link/unlink reports and modifiers in various ways.
    """
    
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
        """Link a single report to a single modifier."""
        serializer = LinkReportToModifierSerializerIn(data=request.data)
        serializer.is_valid(raise_exception=True)
        modifier_id = serializer.validated_data["modifier_id"]
        report_id = serializer.validated_data["report_id"]

        report = get_object_or_404(Report, id=report_id)
        modifier = get_object_or_404(ReportModifier, id=modifier_id)
        
        # Check if relationship already exists
        if report.modifiers.filter(id=modifier_id).exists():
            return Response({
                'meta': {
                    'status': 'already_linked',
                    'message': 'Report and modifier are already linked',
                    'timestamp': timezone.now().isoformat(),
                    'links': {
                        'report': f"{request.build_absolute_uri('/').rstrip('/')}/api/reports/{report_id}/",
                        'modifier': f"{request.build_absolute_uri('/').rstrip('/')}/api/report-modifiers/{modifier_id}/"
                    }
                },
                'data': {
                    'status': 'already_linked',
                    'report_id': report_id,
                    'modifier_id': modifier_id,
                }
            }, status=status.HTTP_200_OK)
        
        report.modifiers.add(modifier)

        return Response({
            'meta': {
                'status': 'success',
                'message': 'Report successfully linked to modifier',
                'timestamp': timezone.now().isoformat(),
                'links': {
                    'report': f"{request.build_absolute_uri('/').rstrip('/')}/api/reports/{report_id}/",
                    'modifier': f"{request.build_absolute_uri('/').rstrip('/')}/api/report-modifiers/{modifier_id}/",
                    'report_modifiers': f"{request.build_absolute_uri('/').rstrip('/')}/api/reports/{report_id}/modifiers/"
                }
            },
            'data': {
                'status': 'success',
                'report_id': report_id,
                'modifier_id': modifier_id,
            }
        }, status=status.HTTP_200_OK)

    @extend_schema(
        request=LinkReportToModifierSerializerIn,
        responses={
            200: LinkReportToModifierSerializerOut,
            400: OpenApiResponse(description="Invalid input"),
            404: OpenApiResponse(description="Report or modifier not found"),
        },
        operation_id="unlink_single_report_modifier",
    )
    @action(detail=False, methods=["delete"], url_path="single")
    def unlink_single(self, request):
        """Unlink a single report from a single modifier."""
        serializer = LinkReportToModifierSerializerIn(data=request.data)
        serializer.is_valid(raise_exception=True)
        modifier_id = serializer.validated_data["modifier_id"]
        report_id = serializer.validated_data["report_id"]

        report = get_object_or_404(Report, id=report_id)
        modifier = get_object_or_404(ReportModifier, id=modifier_id)
        
        if not report.modifiers.filter(id=modifier_id).exists():
            return Response({
                'meta': {
                    'status': 'not_linked',
                    'message': 'Report and modifier are not linked',
                    'timestamp': timezone.now().isoformat(),
                },
                'data': {
                    'status': 'not_linked',
                    'report_id': report_id,
                    'modifier_id': modifier_id,
                }
            }, status=status.HTTP_200_OK)
        
        report.modifiers.remove(modifier)

        return Response({
            'meta': {
                'status': 'success',
                'message': 'Report successfully unlinked from modifier',
                'timestamp': timezone.now().isoformat(),
            },
            'data': {
                'status': 'unlinked',
                'report_id': report_id,
                'modifier_id': modifier_id,
            }
        }, status=status.HTTP_200_OK)

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
        """Link multiple reports to multiple modifiers (creates all combinations)."""
        serializer = LinkMultipleReportsToModifiersIn(data=request.data)
        serializer.is_valid(raise_exception=True)

        reports = serializer.validated_data["reports"]
        modifiers = serializer.validated_data["modifiers"]

        linked_count = 0
        already_linked_count = 0
        
        with transaction.atomic():
            for r in reports:
                for m in modifiers:
                    this_report = get_object_or_404(Report, id=r)
                    this_modifier = get_object_or_404(ReportModifier, id=m)
                    
                    if this_report.modifiers.filter(id=m).exists():
                        already_linked_count += 1
                    else:
                        this_report.modifiers.add(this_modifier)
                        linked_count += 1

        return Response({
            'meta': {
                'status': 'success',
                'message': f'Processed {len(reports)} reports with {len(modifiers)} modifiers',
                'timestamp': timezone.now().isoformat(),
                'statistics': {
                    'total_combinations': len(reports) * len(modifiers),
                    'newly_linked': linked_count,
                    'already_linked': already_linked_count
                }
            },
            'data': {
                'status': 'success',
                'reports': reports,
                'modifiers': modifiers,
                'linked_count': linked_count,
                'already_linked_count': already_linked_count
            }
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"])
    def summary(self, request):
        """Get summary statistics about report-modifier relationships."""
        total_reports = Report.objects.count()
        total_modifiers = ReportModifier.objects.count()
        reports_with_modifiers = Report.objects.filter(modifiers__isnull=False).distinct().count()
        modifiers_with_reports = ReportModifier.objects.filter(reports__isnull=False).distinct().count()
        
        return Response({
            'meta': {
                'endpoint': 'link_summary',
                'timestamp': timezone.now().isoformat(),
            },
            'data': {
                'total_reports': total_reports,
                'total_modifiers': total_modifiers,
                'reports_with_modifiers': reports_with_modifiers,
                'modifiers_with_reports': modifiers_with_reports,
                'reports_without_modifiers': total_reports - reports_with_modifiers,
                'modifiers_without_reports': total_modifiers - modifiers_with_reports,
            }
        })
