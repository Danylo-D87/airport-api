from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny

from airport.models import (
    Country,
    City,
)
from airport.serializers import (
    CountrySerializer,
    CitySerializer,
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