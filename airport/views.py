from rest_framework import viewsets, mixins
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from airport.models import (
    Country,
    City,
    Airport,
    AirplaneType,
    Airplane,
    Crew,
    Route,
    Flight,
    Order,
)
from airport.permissions import IsStaffUser, IsStaffOrOwner
from airport.serializers import (
    CountrySerializer,
    CitySerializer,
    AirportSerializer,
    CrewSerializer,
    RouteSerializer,
    FlightSerializer,
    OrderSerializer,
    AirplaneTypeSerializer,
    AirplaneSerializer,
    OrderListSerializer,
)


class CountryViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    """
    Accessible for viewing by all users; editing,
    adding, and deleting are managed via the admin panel.
    """

    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = (AllowAny,)


class CityViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    """
    Accessible for viewing by all users; editing,
    adding, and deleting are managed via the admin panel.
    """

    queryset = City.objects.select_related("country").all()
    serializer_class = CitySerializer
    permission_classes = (AllowAny,)


class AirportViewSet(viewsets.ModelViewSet):
    queryset = Airport.objects.select_related("city").all()
    serializer_class = AirportSerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]
        return [IsStaffUser()]


class AirplaneTypeViewSet(viewsets.ModelViewSet):
    queryset = AirplaneType.objects.all()
    serializer_class = AirplaneTypeSerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]
        return [IsStaffUser()]


class AirplaneViewSet(viewsets.ModelViewSet):
    queryset = Airplane.objects.select_related("airplane_type").all()
    serializer_class = AirplaneSerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]
        return [IsStaffUser()]


class CrewViewSet(viewsets.ModelViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]
        return [IsStaffUser()]


class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.select_related("source", "destination").all()
    serializer_class = RouteSerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]
        return [IsStaffUser()]


class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.all().select_related(
        "route",
        "airplane"
    ).prefetch_related("crew")
    serializer_class = FlightSerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]
        return [IsStaffUser()]


class OrderViewSet(mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related("tickets__flight")

    def get_serializer_class(self):
        if self.action == "list":
            return OrderListSerializer
        return OrderSerializer

