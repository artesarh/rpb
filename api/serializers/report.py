from rest_framework import serializers
from api.models.report import Report, ReportModifier
from api.models.event import EventGroup
from api.serializers.event import EventGroupDetailedSerializer


class ReportModifierSerializer(serializers.ModelSerializer):
    quarter = serializers.ReadOnlyField()
    year = serializers.ReadOnlyField()
    month = serializers.ReadOnlyField()
    day = serializers.ReadOnlyField()

    class Meta:
        model = ReportModifier
        fields = ["id", "as_at_date", "fx_date", "quarter", "year", "month", "day"]


class ReportSerializer(serializers.HyperlinkedModelSerializer):
    modifiers = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name="api:report-modifier-detail",
        lookup_field="id",
        lookup_url_kwarg="modifier_id",
    )
    event_group = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name="api:event-group-detail",
        lookup_field="id",
        lookup_url_kwarg="pk",
    )

    class Meta:
        model = Report
        fields = "__all__"
        extra_kwargs = {"url": {"view_name": "api:report-detail"}}


class _ReportWithoutModifierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = "__all__"  # Include all model fields
        extra_kwargs = {
            # Ignore reverse relation
            "modifiers": {"read_only": True, "required": False}
        }


class ReportWithModifierSerializer(serializers.Serializer):
    report = _ReportWithoutModifierSerializer()
    modifier = ReportModifierSerializer()


class ReportWithModifiersListSerializer(serializers.Serializer):
    report = _ReportWithoutModifierSerializer()
    modifiers = ReportModifierSerializer(many=True)


class ReportWithAllSerializer(serializers.Serializer):
    report = _ReportWithoutModifierSerializer()
    eventgroup = EventGroupDetailedSerializer()
    modifier = ReportModifierSerializer(required=False)
