from django.test import TestCase
from airport.serializers import RouteSerializer, TicketSerializer, FlightSerializer
from django.utils import timezone
from datetime import timedelta
from airport.models import Airplane, AirplaneType, Route, Flight, Airport, City, Country, Crew, Ticket, Order
from django.contrib.auth import get_user_model

User = get_user_model()

class RouteSerializerTest(TestCase):
    def setUp(self):
        self.country = Country.objects.create(name="Ukraine")
        self.city = City.objects.create(name="Kyiv", country=self.country)
        self.airport1 = Airport.objects.create(name="Boryspil", city=self.city)
        self.airport2 = Airport.objects.create(name="Zhuliany", city=self.city)

    def test_valid_route(self):
        data = {
            "source_id": self.airport1.pk,
            "destination_id": self.airport2.pk,
            "distance": 300
        }
        serializer = RouteSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_invalid_route_same_source_destination(self):
        data = {
            "source_id": self.airport1.pk,
            "destination_id": self.airport1.pk,
            "distance": 100
        }
        serializer = RouteSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("non_field_errors", serializer.errors)
        self.assertEqual(
            serializer.errors["non_field_errors"][0],
            "Source and destination airports must be different."
        )

class FlightSerializerTest(TestCase):
    def setUp(self):
        country = Country.objects.create(name="Ukraine")
        city = City.objects.create(name="Kyiv", country=country)
        airport1 = Airport.objects.create(name="Boryspil", city=city)
        airport2 = Airport.objects.create(name="Zhuliany", city=city)
        self.route = Route.objects.create(source=airport1, destination=airport2, distance=300)
        self.airplane_type = AirplaneType.objects.create(name="Boeing 737")
        self.airplane = Airplane.objects.create(
            name="Boeing 737-800", rows=30, seats_in_rows=6, airplane_type=self.airplane_type
        )
        self.crew = Crew.objects.create(first_name="John", last_name="Doe")

    def test_valid_flight(self):
        departure = timezone.now() + timedelta(days=1)
        arrival = departure + timedelta(hours=2)
        data = {
            "route": self.route.pk,
            "airplane": self.airplane.name,
            "departure_time": departure,
            "arrival_time": arrival,
            "crew_ids": [self.crew.pk]
        }
        serializer = FlightSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_departure_in_past(self):
        departure = timezone.now() - timedelta(days=1)
        arrival = timezone.now() + timedelta(hours=1)
        data = {
            "route": self.route.pk,
            "airplane": self.airplane.name,
            "departure_time": departure,
            "arrival_time": arrival,
            "crew_ids": [self.crew.pk]
        }
        serializer = FlightSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("departure_time", serializer.errors)
        self.assertEqual(serializer.errors["departure_time"][0], "Час вильоту не може бути в минулому.")

    def test_arrival_before_departure(self):
        departure = timezone.now() + timedelta(days=1)
        arrival = departure - timedelta(hours=1)
        data = {
            "route": self.route.pk,
            "airplane": self.airplane.name,
            "departure_time": departure,
            "arrival_time": arrival,
            "crew_ids": [self.crew.pk]
        }
        serializer = FlightSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("non_field_errors", serializer.errors)
        self.assertEqual(serializer.errors["non_field_errors"][0], "Час прильоту має бути пізніше часу вильоту.")


class TicketSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="testuser@example.com", password="12345")
        country = Country.objects.create(name="Ukraine")
        city = City.objects.create(name="Kyiv", country=country)
        airport1 = Airport.objects.create(name="Boryspil", city=city)
        airport2 = Airport.objects.create(name="Zhuliany", city=city)
        route = Route.objects.create(source=airport1, destination=airport2, distance=300)
        airplane_type = AirplaneType.objects.create(name="Boeing 737")
        airplane = Airplane.objects.create(
            name="Boeing 737-800", rows=30, seats_in_rows=6, airplane_type=airplane_type
        )
        self.flight = Flight.objects.create(
            route=route,
            airplane=airplane,
            departure_time=timezone.now() + timedelta(days=1),
            arrival_time=timezone.now() + timedelta(days=1, hours=2),
        )
        self.order = Order.objects.create(user=self.user)

    def test_valid_ticket(self):
        data = {
            "row_number": 5,
            "seat_number": 3,
            "flight": self.flight.pk,
        }
        serializer = TicketSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_row_number_out_of_range(self):
        data = {
            "row_number": 31,  # поза межами рядів літака
            "seat_number": 3,
            "flight": self.flight.pk,
        }
        serializer = TicketSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("non_field_errors", serializer.errors)
        self.assertEqual(serializer.errors["non_field_errors"][0], "Row number must be between 1 and 30.")

    def test_seat_number_out_of_range(self):
        data = {
            "row_number": 5,
            "seat_number": 7,
            "flight": self.flight.pk,
        }
        serializer = TicketSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("non_field_errors", serializer.errors)
        self.assertEqual(serializer.errors["non_field_errors"][0], "Seat number must be between 1 and 6.")

    def test_seat_already_booked(self):
        Ticket.objects.create(
            flight=self.flight,
            row_number=5,
            seat_number=3,
            order=self.order
        )
        data = {
            "row_number": 5,
            "seat_number": 3,
            "flight": self.flight.pk,
        }
        serializer = TicketSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        errors = serializer.errors
        if "non_field_errors" in errors:
            self.assertEqual(errors["non_field_errors"][0], "The fields flight, row_number, seat_number must make a unique set."
)
        else:
            self.fail(f"Expected 'non_field_errors' but got: {errors}")


class OrderSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="testuser@example.com", password="12345")
        country = Country.objects.create(name="Ukraine")
        city = City.objects.create(name="Kyiv", country=country)
        airport1 = Airport.objects.create(name="Boryspil", city=city)
        airport2 = Airport.objects.create(name="Zhuliany", city=city)
        route = Route.objects.create(source=airport1, destination=airport2, distance=300)
        airplane_type = AirplaneType.objects.create(name="Boeing 737")
        airplane = Airplane.objects.create(
            name="Boeing 737-800", rows=30, seats_in_rows=6, airplane_type=airplane_type
        )
        self.flight = Flight.objects.create(
            route=route,
            airplane=airplane,
            departure_time=timezone.now() + timedelta(days=1),
            arrival_time=timezone.now() + timedelta(days=1, hours=2)
        )
