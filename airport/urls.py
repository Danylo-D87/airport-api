from django.urls import path, include
from rest_framework import routers
from airport.views import (
    CountryViewSet,
    CityViewSet,
    AirportViewSet,
)


router = routers.DefaultRouter()
router.register("countries", CountryViewSet, basename="country")
router.register("cities", CityViewSet, basename="city")
router.register("airports", AirportViewSet, basename="airport")

urlpatterns = [
    path("", include(router.urls)),
]

app_name = "airport"
