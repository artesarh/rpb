# reporting/admin.py
from django.contrib import admin
from unfold.admin import ModelAdmin
from api.models import (
    Report,
    ReportModifier,
    Event,
    GeoEvent,
    RingEvent,
    Job,
    EventGroup,
)


@admin.register(Report)
class ReportAdmin(ModelAdmin):
    exclude_fields = ["id", "updated_at"]
    list_display = [
        field.name
        for field in Report._meta.get_fields()
        if field.name not in exclude_fields
    ]
    exclude = exclude_fields  # Use exclude for form fields
    list_filter = ("created_at", "user")
    search_fields = ("title", "content")
