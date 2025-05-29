from rest_framework import serializers
from api.models.report import Report, ReportModifier
from api.models.job import Job


class JobSerializer(serializers.ModelSerializer):
    report = serializers.PrimaryKeyRelatedField(queryset=Report.objects.all())
    report_modifier = serializers.PrimaryKeyRelatedField(
        queryset=ReportModifier.objects.all(), allow_null=True
    )

    class Meta:
        model = Job
        fields = ["id", "report", "report_modifier", "created", "updated"]
