# api/admin.py
from django.contrib import admin
from .models.event import Event, EventGroup, RingEvent, BoxEvent, GeoEvent
from .models.report import Report, ReportModifier
from .models.job import Job


# Inline for Jobs related to Report
class JobInline(admin.TabularInline):
    model = Job
    extra = 0
    fields = ("fireant_jobid", "created", "updated")
    readonly_fields = ("created", "updated")


# Inline for Events in EventGroup
class EventInline(admin.TabularInline):
    model = EventGroup.events.through
    extra = 1
    verbose_name = "Event"
    verbose_name_plural = "Events"


# Inline for Reports in ReportModifier
class ReportInline(admin.TabularInline):
    model = ReportModifier.reports.through
    extra = 1
    verbose_name = "Report"
    verbose_name_plural = "Reports"


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "zone", "is_valid")
    list_filter = ("is_valid", "zone")
    search_fields = ("name", "description", "zone")
    readonly_fields = ("id",)


@admin.register(EventGroup)
class EventGroupAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "created", "updated")
    list_filter = ("created",)
    search_fields = ("name",)
    readonly_fields = ("id", "created", "updated")
    inlines = [EventInline]


@admin.register(RingEvent)
class RingEventAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "latitude",
                    "longitude", "radius", "is_valid")
    list_filter = ("is_valid",)
    search_fields = ("name", "description")
    readonly_fields = ("id",)


@admin.register(BoxEvent)
class BoxEventAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "max_lat",
        "min_lat",
        "max_lon",
        "min_lon",
        "is_valid",
    )
    list_filter = ("is_valid",)
    search_fields = ("name", "description")
    readonly_fields = ("id",)


@admin.register(GeoEvent)
class GeoEventAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "country", "area", "subarea", "is_valid")
    list_filter = ("is_valid", "country")
    search_fields = ("name", "description", "country", "area", "subarea")
    readonly_fields = ("id",)


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "peril",
        "event_group",
        "is_valid",
        "created",
        "updated",
    )
    list_filter = ("is_valid", "peril", "priority", "created")
    search_fields = ("name", "peril", "event_group__name")
    fieldsets = (
        (None, {"fields": ("name", "peril", "event_group", "is_valid")}),
        (
            "Configuration",
            {
                "fields": (
                    "dr",
                    "cron",
                )
            },
        ),
        (
            "Optionals",
            {
                "fields": (
                    "cob",
                    "priority",
                    "ncores",
                    "loss_perspective",
                )
            },
        ),
        (
            "Bool Options",
            {
                "fields": (
                    "is_apply_calibration",
                    "is_apply_inflation",
                    "is_tag_outwards_ptns",
                    "is_location_breakout",
                    "is_ignore_missing_lat_lon",
                )
            },
        ),
        ("Node IDs", {"fields": ("gross_node_id",
         "net_node_id", "rollup_context_id")}),
        (
            "Thresholds",
            {
                "fields": (
                    "dynamic_ring_loss_threshold",
                    "blast_radius",
                    "no_overlap_radius",
                    "location_breakout_max_events",
                    "location_breakout_max_locations",
                )
            },
        ),
        ("Timestamps", {"fields": ("created", "updated")}),
    )
    readonly_fields = ("id", "created", "updated")


@admin.register(ReportModifier)
class ReportModifierAdmin(admin.ModelAdmin):
    list_display = ("id", "as_at_date", "fx_date", "year", "quarter")
    list_filter = ("as_at_date",)
    search_fields = ("as_at_date", "fx_date")
    readonly_fields = ("id",)
    inlines = [ReportInline]


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ("id", "report", "fireant_jobid", "created", "updated")
    list_filter = ("created", "report")
    search_fields = ("report__name", "fireant_jobid")
    readonly_fields = ("id", "created", "updated")
