from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny

from airport.models import (
    Country,
    City,
    Airport, AirplaneType,
)
from airport.permissions import IsStaffUser
from airport.serializers import (
    CountrySerializer,
    CitySerializer,
    AirportSerializer,
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
            return [AllowAny]
        return [IsStaffUser]


class AirplaneTypeViewSet(viewsets.ModelViewSet):
    queryset = AirplaneType.objects.all()
    serializer_class = AirportSerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [AllowAny]
        return [IsStaffUser]

