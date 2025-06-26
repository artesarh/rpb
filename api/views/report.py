from api.serializers import (
    ReportSerializer,
    ReportModifierSerializer,
    ReportWithAllSerializer,
    ReportWithModifierSerializer,
    ReportWithModifiersListSerializer,
    EventGroupSerializer,
)
from api.models import Report, ReportModifier
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import (
    extend_schema,
    OpenApiParameter,
    OpenApiResponse,
    OpenApiExample,
)
from rest_framework.exceptions import NotFound
from django.utils import timezone
from .core import BaseViewSetMixin


class ReportViewSet(BaseViewSetMixin, viewsets.ModelViewSet):
    queryset = Report.objects.select_related("event_group").prefetch_related(
        "modifiers", "jobs"
    )
    serializer_class = ReportSerializer
    http_method_names = ["get", "post", "patch", "put", "delete"]
    
    # Enhanced filtering and search
    filterset_fields = ['peril', 'is_valid', 'event_group', 'priority', 'loss_perspective']
    search_fields = ['name', 'peril', 'event_group__name']
    ordering_fields = ['name', 'peril', 'created', 'updated', 'priority']
    ordering = ['-created']

    def get_queryset(self):
        return self.queryset

    @extend_schema(
        request=ReportSerializer,
        responses={
            201: ReportSerializer,
            400: OpenApiResponse(description="Invalid input data"),
        },
        examples=[
            OpenApiExample(
                "Valid Report Creation",
                value={
                    "name": "Test Report",
                    "peril": "Flood",
                    "dr": 1.0,
                    "event_group": None,
                    "cron": "0 0 * * *",
                    "cob": None,
                    "loss_perspective": "Gross",
                    "is_apply_calibration": True,
                    "is_apply_inflation": True,
                    "is_tag_outwards_ptns": False,
                    "is_location_breakout": False,
                    "is_ignore_missing_lat_lon": True,
                    "location_breakout_max_events": 500000,
                    "location_breakout_max_locations": 1000000,
                    "priority": "AboveNormal",
                    "ncores": 24,
                    "gross_node_id": None,
                    "net_node_id": None,
                    "rollup_context_id": 42,
                    "dynamic_ring_loss_threshold": 5000000,
                    "blast_radius": 50.0,
                    "no_overlap_radius": 50.0,
                    "is_valid": True,
                },
                description="Example of a valid POST request to create a Report",
            ),
        ],
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        request=ReportSerializer,
        responses={
            200: ReportSerializer,
            400: OpenApiResponse(description="Invalid input data"),
            404: OpenApiResponse(description="Report not found"),
        },
        examples=[
            OpenApiExample(
                "Partial Update Report",
                value={"event_group": 1},
                description="Example of a PATCH request to update the event_group field of a Report.",
            ),
        ],
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

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
        return Response({
            'meta': {
                'report_id': report.id,
                'modifier_id': modifier.id,
                'links': {
                    'report': f"{request.build_absolute_uri('/').rstrip('/')}/api/reports/{report.id}/",
                    'modifier': f"{request.build_absolute_uri('/').rstrip('/')}/api/report-modifiers/{modifier.id}/"
                }
            },
            'data': serializer.data
        })

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
        return Response({
            'meta': {
                'report_id': report.id,
                'modifiers_count': modifiers.count(),
                'links': {
                    'report': f"{request.build_absolute_uri('/').rstrip('/')}/api/reports/{report.id}/",
                }
            },
            'data': serializer.data
        })

    @extend_schema(
        responses={
            200: ReportWithAllSerializer,
            404: OpenApiResponse(description="Report or modifiers not found"),
        },
        operation_id="get_report_with_eventdetail_modifier",
    )
    @action(detail=True, methods=["get"], url_path="modifier/(?P<modifier_id>\d+)/all")
    def get_report_with_eventdetail_modifier(self, request, pk=None, modifier_id=None):
        """Get a report with its event group details and a specific modifier."""
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
        return Response({
            'meta': {
                'report_id': report.id,
                'event_group_id': eventgroup.id,
                'modifier_id': modifier.id,
                'links': {
                    'report': f"{request.build_absolute_uri('/').rstrip('/')}/api/reports/{report.id}/",
                    'event_group': f"{request.build_absolute_uri('/').rstrip('/')}/api/event-groups/{eventgroup.id}/",
                    'modifier': f"{request.build_absolute_uri('/').rstrip('/')}/api/report-modifiers/{modifier.id}/"
                }
            },
            'data': serializer.data
        })

    @action(detail=True, methods=["get"])
    def jobs(self, request, pk=None):
        """Get all jobs associated with this report."""
        report = self.get_object()
        jobs = report.jobs.all()
        
        from api.serializers.job import JobSerializer
        serializer = JobSerializer(jobs, many=True, context={'request': request})
        
        return Response({
            'meta': {
                'report_id': report.id,
                'jobs_count': jobs.count(),
                'links': {
                    'report': f"{request.build_absolute_uri('/').rstrip('/')}/api/reports/{report.id}/",
                }
            },
            'data': serializer.data
        })

    @action(detail=False, methods=["get"])
    def summary(self, request):
        """Get summary statistics about reports."""
        queryset = self.filter_queryset(self.get_queryset())
        
        total_reports = queryset.count()
        valid_reports = queryset.filter(is_valid=True).count()
        perils = queryset.values_list('peril', flat=True).distinct()
        
        return Response({
            'meta': {
                'endpoint': 'reports_summary',
                'generated_at': timezone.now().isoformat()
            },
            'data': {
                'total_reports': total_reports,
                'valid_reports': valid_reports,
                'invalid_reports': total_reports - valid_reports,
                'unique_perils': list(perils),
                'perils_count': len(perils)
            }
        })
