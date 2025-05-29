from datetime import timezone

from rest_framework import serializers
from .models import (
    Country,
    City,
    Airport,
    AirplaneType,
    Airplane,
    Crew,
    Route,
    Flight,
    Ticket,
    Order,
)


class CountrySerializer(serializers.ModelSerializer):

    class Meta:
        model = Country
        fields = ("id", "name")


class CitySerializer(serializers.ModelSerializer):
    country = serializers.SlugRelatedField(
        slug_field="name",
        read_only=True,
    )

    class Meta:
        model = City
        fields = ("id", "name", "country")


class AirportSerializer(serializers.ModelSerializer):
    city = serializers.SlugRelatedField(
        slug_field="name",
        read_only=True,
    )

    class Meta:
        model = Airport
        fields = ("id", "name", "city")


class AirplaneTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = AirplaneType
        fields = ("id", "name")


class AirplaneSerializer(serializers.ModelSerializer):
    airplane_type = serializers.StringRelatedField()

    class Meta:
        model = Airplane
        fields = ("id", "name","rows", "seats_in_rows", "airplane_type")


class CrewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Crew
        fields = ("id", "first_name", "last_name")


class RouteSerializer(serializers.ModelSerializer):
    source = serializers.SlugRelatedField(
        slug_field="name",
        read_only=True,
    )
    destination = serializers.SlugRelatedField(
        slug_field="name",
        read_only=True,
    )

    class Meta:
        model = Route
        fields = ("id", "source", "destination", "distance")


class FlightSerializer(serializers.ModelSerializer):
    route = serializers.SlugRelatedField(
        slug_field="name",
        read_only=True,
    )
    airplane = serializers.SlugRelatedField(
        slug_field="name",
        read_only=True,
    )
    crew = CrewSerializer(many=True, read_only=True)

    class Meta:
        model = Flight
        fields = ("id", "route", "airplane", "departure_time", "arrival_time", "crew")

    def validate_departure_time(self, value):
        if value < timezone.now():
            raise serializers.ValidationError("Час вильоту не може бути в минулому.")
        return value

    def validate(self, data):
        # Перевірка, що arrival_time > departure_time
        departure = data.get("departure_time", getattr(self.instance, "departure_time", None))
        arrival = data.get("arrival_time", getattr(self.instance, "arrival_time", None))
        if arrival and departure and arrival <= departure:
            raise serializers.ValidationError("Час прильоту має бути пізніше часу вильоту.")
        return data
