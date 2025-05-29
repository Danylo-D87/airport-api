from django.db import transaction
from django.utils import timezone

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
        queryset=City.objects.all(),
    )

    class Meta:
        model = Airport
        fields = ("id", "name", "city")


class AirplaneTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = AirplaneType
        fields = ("id", "name")


class AirplaneSerializer(serializers.ModelSerializer):
    airplane_type = serializers.SlugRelatedField(
        slug_field="name",
        queryset=AirplaneType.objects.all(),
    )

    class Meta:
        model = Airplane
        fields = ("id", "name","rows", "seats_in_rows", "airplane_type")


class CrewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Crew
        fields = ("id", "first_name", "last_name")


class RouteSerializer(serializers.ModelSerializer):
    source = AirportSerializer(read_only=True)
    destination = AirportSerializer(read_only=True)

    source_id = serializers.PrimaryKeyRelatedField(
        queryset=Airport.objects.all(), write_only=True, source="source"
    )
    destination_id = serializers.PrimaryKeyRelatedField(
        queryset=Airport.objects.all(), write_only=True, source="destination"
    )

    class Meta:
        model = Route
        fields = ("id", "source", "destination", "source_id", "destination_id", "distance")

    def validate(self, data):
        if data["source"] == data["destination"]:
            raise serializers.ValidationError("Source and destination airports must be different.")
        return data



class FlightSerializer(serializers.ModelSerializer):
    route = serializers.SlugRelatedField(
        slug_field="id",
        queryset=Route.objects.all()
    )
    airplane = serializers.SlugRelatedField(
        slug_field="name",
        queryset=Airplane.objects.all()
    )
    crew = serializers.StringRelatedField(many=True, read_only=True)
    crew_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Crew.objects.all(),
        write_only=True,
        source="crew"
    )

    class Meta:
        model = Flight
        fields = ("id", "route", "airplane", "departure_time", "arrival_time", "crew", "crew_ids")

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


class TicketSerializer(serializers.ModelSerializer):
    flight = serializers.PrimaryKeyRelatedField(queryset=Flight.objects.all())

    class Meta:
        model = Ticket
        fields = ("row_number", "seat_number", "flight")

    def validate(self, data):
        # Валідація, що місце не зайняте на конкретному рейсі
        flight = data.get("flight")
        row = data.get("row_number")
        seat = data.get("seat_number")

        # Перевірка, чи місце не зайняте
        if Ticket.objects.filter(flight=flight, row_number=row, seat_number=seat).exists():
            raise serializers.ValidationError("This seat is already booked on this flight.")

        # Перевірка, чи ряд та місце у межах літака
        airplane = flight.airplane
        if row < 1 or row > airplane.rows:
            raise serializers.ValidationError(f"Row number must be between 1 and {airplane.rows}.")
        if seat < 1 or seat > airplane.seats_in_rows:
            raise serializers.ValidationError(f"Seat number must be between 1 and {airplane.seats_in_rows}.")

        return data

class TicketListSerializer(serializers.ModelSerializer):
    # Для виводу можна показати деталі рейсу, наприклад, id
    flight = serializers.StringRelatedField()

    class Meta:
        model = Ticket
        fields = ("row_number", "seat_number", "flight")


class OrderSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True, allow_empty=False)

    class Meta:
        model = Order
        fields = ("id", "created_at", "tickets")

    def create(self, validated_data):
        tickets_data = validated_data.pop("tickets")
        user = self.context["request"].user

        flight_ticket_pairs = set()

        # Перевірка на дублікати у запиті (щоб не було однакових місць у одному замовленні)
        for ticket in tickets_data:
            flight = ticket["flight"]
            row = ticket["row_number"]
            seat = ticket["seat_number"]

            if (flight, row, seat) in flight_ticket_pairs:
                raise serializers.ValidationError(f"Duplicate seat {row}-{seat} for flight {flight} in request.")
            flight_ticket_pairs.add((flight, row, seat))

        # Перевірка, чи місце не зайняте у базі
        for flight, row, seat in flight_ticket_pairs:
            if Ticket.objects.filter(flight=flight, row_number=row, seat_number=seat).exists():
                raise serializers.ValidationError(f"Seat {row}-{seat} is already booked on flight {flight}.")

        with transaction.atomic():
            order = Order.objects.create(user=user, **validated_data)
            for ticket_data in tickets_data:
                Ticket.objects.create(order=order, **ticket_data)

        return order




class OrderListSerializer(serializers.ModelSerializer):
    tickets = TicketListSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ("id", "created_at", "tickets")


