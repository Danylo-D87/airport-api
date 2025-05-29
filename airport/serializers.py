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
