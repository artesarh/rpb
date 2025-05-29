# api/admin.py
from django.contrib import admin
from unfold.admin import ModelAdmin
from .models.report import Report, ReportModifier
from .models.event import Event, EventGroup, RingEvent, BoxEvent, GeoEvent
from .models.job import Job


@admin.register(Report)
class ReportAdmin(ModelAdmin):
    list_filter = (
        "created",
        "is_valid",
        "priority",
        "is_apply_calibration",
        "is_apply_inflation",
    )
    search_fields = ("name", "peril", "cob")


@admin.register(ReportModifier)
class ReportModifierAdmin(ModelAdmin):
    list_filter = ("as_at_date",)
    search_fields = ("as_at_date",)
    readonly_fields = ["quarter", "year", "month", "day"]


@admin.register(Event)
class EventAdmin(ModelAdmin):
    list_filter = ("is_valid",)
    search_fields = ("name", "description")


@admin.register(EventGroup)
class EventGroupAdmin(ModelAdmin):
    list_filter = ("created",)
    search_fields = ("name",)


@admin.register(RingEvent)
class RingEventAdmin(ModelAdmin):
    list_filter = ("is_valid",)
    search_fields = ("name", "description")


@admin.register(BoxEvent)
class BoxEventAdmin(ModelAdmin):
    list_filter = ("is_valid",)
    search_fields = ("name", "description")


@admin.register(GeoEvent)
class GeoEventAdmin(ModelAdmin):
    list_filter = ("is_valid",)
    search_fields = ("name", "description", "country", "area")


@admin.register(Job)
class JobAdmin(ModelAdmin):
    list_filter = ("created",)
    search_fields = ("report__name",)
