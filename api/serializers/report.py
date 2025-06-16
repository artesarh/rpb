from rest_framework import serializers
from api.models.report import Report, ReportModifier
from api.models.event import EventGroup
from api.serializers.event import (
    EventGroupDetailedSerializer,
)


class ReportModifierSerializer(serializers.ModelSerializer):
    quarter = serializers.ReadOnlyField()
    year = serializers.ReadOnlyField()
    month = serializers.ReadOnlyField()
    day = serializers.ReadOnlyField()

    class Meta:
        model = ReportModifier
        fields = ["id", "as_at_date", "fx_date", "quarter", "year", "month", "day"]


class ReportSerializer(serializers.ModelSerializer):
    event_group = serializers.PrimaryKeyRelatedField(
        queryset=EventGroup.objects.all(), many=False
    )
    cron = serializers.CharField(max_length=50, allow_blank=True, allow_null=True)
    modifiers = ReportModifierSerializer(
        many=True, read_only=True
    )  # Removed source='modifiers'

    class Meta:
        model = Report
        fields = "__all__"


class ReportWithoutModifierSerializer(serializers.ModelSerializer):
    """
    Report but without nested modifier key
    """

    class Meta:
        model = Report
        fields = "__all__"  # Include all fields by default
        extra_kwargs = {
            "modifiers": {"read_only": True, "required": False}
        }  # Exclude from output

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data.pop("modifiers", None)  # Ensure modifiers is removed from the response
        return data


class ReportWithModifierSerializer(serializers.Serializer):
    """
    Report with modifier at top level
    """

    report = ReportWithoutModifierSerializer()
    modifier = ReportModifierSerializer()


class ReportWithEventGroupDetailSerializer(serializers.Serializer):
    """ """

    report = ReportWithoutModifierSerializer()
    eventgroup = EventGroupDetailedSerializer()


class ReportWithEventGroupDetailModifierSerializer(
    ReportWithEventGroupDetailSerializer
):
    """Add modifier to inherited class"""

    modifier = ReportModifierSerializer()


class LinkReportToModifierSerializer(serializers.Serializer):
    status = serializers.CharField()
    report_id = serializers.IntegerField()
    modifier_id = serializers.IntegerField()
