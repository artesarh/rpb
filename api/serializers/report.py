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
        # Ensure modifiers is removed from the response
        data.pop("modifiers", None)
        return data


class ReportWithModifierSerializerOut(serializers.Serializer):
    report = ReportWithoutModifierSerializer()
    modifier = ReportModifierSerializer()


class ReportWithModifierSerializerIn(serializers.Serializer):
    """
    Report with modifiers at top level
    """

    report = ReportWithoutModifierSerializer()
    modifier = ReportModifierSerializer()


class ReportWithModifierListSerializerOut(serializers.Serializer):
    report = ReportWithoutModifierSerializer()
    modifiers = ReportModifierSerializer(many=True)


class ReportWithModifierListSerializerIn(serializers.Serializer):
    """
    Report with modifiers at top level
    """

    report = ReportWithoutModifierSerializer()
    modifiers = ReportModifierSerializer(many=True)


class ReportWithEventGroupDetailSerializer(serializers.Serializer):
    """ """

    report = ReportWithoutModifierSerializer()
    eventgroup = EventGroupDetailedSerializer()


class ReportWithEventGroupDetailModifierSerializer(
    ReportWithEventGroupDetailSerializer
):
    """Add modifier to inherited class"""

    modifier = ReportModifierSerializer()
