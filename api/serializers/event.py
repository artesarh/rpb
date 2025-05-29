from rest_framework import serializers
from api.models.event import Event, EventGroup, RingEvent, BoxEvent, GeoEvent
import re


def validate_cron(value):
    if value and not re.match(
        r"^[0-9*/,-]+\s+[0-9*/,-]+\s+[0-9*/,-]+\s+[0-9*/,-]+\s+[0-9*/,-]+$", value
    ):
        raise serializers.ValidationError("Invalid cron syntax")


def validate_latitude(value):
    if not -90 <= value <= 90:
        raise serializers.ValidationError(
            "Latitude must be between -90 and 90 degrees."
        )


def validate_longitude(value):
    if not -180 <= value <= 180:
        raise serializers.ValidationError(
            "Longitude must be between -180 and 180 degrees."
        )


class EventSerializer(serializers.ModelSerializer):
    event_type = serializers.SerializerMethodField()

    def get_event_type(self, obj):
        if hasattr(obj, "ringevent") and obj.ringevent:
            return "ring"
        elif hasattr(obj, "boxevent") and obj.boxevent:
            return "box"
        elif hasattr(obj, "geoevent") and obj.geoevent:
            return "geo"
        return "base"

    class Meta:
        model = Event
        fields = ["id", "name", "description", "is_valid", "event_type"]


class RingEventSerializer(serializers.ModelSerializer):
    event_type = serializers.SerializerMethodField()

    def get_event_type(self, obj):
        return "ring"

    latitude = serializers.FloatField(validators=[validate_latitude])
    longitude = serializers.FloatField(validators=[validate_longitude])
    radius = serializers.FloatField(min_value=0)

    class Meta:
        model = RingEvent
        fields = [
            "id",
            "name",
            "description",
            "is_valid",
            "latitude",
            "longitude",
            "radius",
            "event_type",
        ]


class BoxEventSerializer(serializers.ModelSerializer):
    event_type = serializers.SerializerMethodField()

    def get_event_type(self, obj):
        return "box"

    max_lat = serializers.FloatField(validators=[validate_latitude])
    min_lat = serializers.FloatField(validators=[validate_latitude])
    max_lon = serializers.FloatField(validators=[validate_longitude])
    min_lon = serializers.FloatField(validators=[validate_longitude])

    def validate(self, data):
        if data["max_lat"] <= data["min_lat"]:
            raise serializers.ValidationError(
                "max_lat must be greater than min_lat.")
        if data["max_lon"] <= data["min_lon"]:
            raise serializers.ValidationError(
                "max_lon must be greater than min_lon.")
        return data

    class Meta:
        model = BoxEvent
        fields = [
            "id",
            "name",
            "description",
            "is_valid",
            "max_lat",
            "min_lat",
            "max_lon",
            "min_lon",
            "event_type",
        ]


class GeoEventSerializer(serializers.ModelSerializer):
    event_type = serializers.SerializerMethodField()

    def get_event_type(self, obj):
        return "geo"

    class Meta:
        model = GeoEvent
        fields = [
            "id",
            "name",
            "description",
            "is_valid",
            "country",
            "area",
            "subarea",
            "subarea2",
            "event_type",
        ]


class EventGroupSerializer(serializers.ModelSerializer):
    events = EventSerializer(many=True, read_only=True)
    event_ids = serializers.PrimaryKeyRelatedField(
        queryset=Event.objects.all(), many=True, write_only=True, source="events"
    )

    class Meta:
        model = EventGroup
        fields = ["id", "name", "events", "event_ids", "created", "updated"]

    def validate(self, data):
        event_ids = data.get("event_ids", [])
        if len(event_ids) > 1:  # Check only if more than one event
            event_types = set()
            for event_id in event_ids:
                # Access the Event instance
                event = Event.objects.get(id=event_id.id)
                if hasattr(event, "ringevent") and event.ringevent:
                    event_types.add("ring")
                elif hasattr(event, "boxevent") and event.boxevent:
                    event_types.add("box")
                elif hasattr(event, "geoevent") and event.geoevent:
                    event_types.add("geo")
                else:
                    event_types.add("base")
            if len(event_types) > 1:
                raise serializers.ValidationError(
                    "All events in an EventGroup must be of the same type."
                )
        return data


class EventGroupDetailedSerializer(serializers.ModelSerializer):
    events = serializers.SerializerMethodField()

    class Meta:
        model = EventGroup
        fields = ["id", "name", "created", "updated", "events"]

    def get_events(self, obj):
        events = obj.events.all()
        serialized_events = []
        for event in events:
            if hasattr(event, "geoevent") and event.geoevent:
                serialized_events.append(
                    GeoEventSerializer(event.geoevent).data)
            elif hasattr(event, "ringevent") and event.ringevent:
                serialized_events.append(
                    RingEventSerializer(event.ringevent).data)
            elif hasattr(event, "boxevent") and event.boxevent:
                serialized_events.append(
                    BoxEventSerializer(event.boxevent).data)
            else:
                serialized_events.append(EventSerializer(event).data)
        return serialized_events
