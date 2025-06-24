from rest_framework import serializers


class LinkReportToModifierSerializerOut(serializers.Serializer):
    status = serializers.CharField()
    report_id = serializers.IntegerField()
    modifier_id = serializers.IntegerField()


class LinkReportToModifierSerializerIn(serializers.Serializer):
    report_id = serializers.IntegerField()
    modifier_id = serializers.IntegerField()


class LinkMultipleReportsToModifiersIn(serializers.Serializer):
    reports = serializers.ListField(child=serializers.IntegerField(), allow_empty=False)
    modifiers = serializers.ListField(
        child=serializers.IntegerField(), allow_empty=False
    )


class LinkMultipleReportsToModifiersOut(serializers.Serializer):
    """List of reports and modifiers with status"""

    status = serializers.CharField(max_length=100)
    reports = serializers.ListField(child=serializers.IntegerField())
    modifiers = serializers.ListField(child=serializers.IntegerField())
