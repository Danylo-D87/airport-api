from django.urls import path, include
from rest_framework import routers
from airport.views import (
    CountryViewSet,
    CityViewSet,
    AirportViewSet,
    AirplaneTypeViewSet,
    AirplaneViewSet,
    CrewViewSet,
    RouteViewSet,
)


router = routers.DefaultRouter()
router.register("countries", CountryViewSet, basename="country")
router.register("cities", CityViewSet, basename="city")
router.register("airports", AirportViewSet, basename="airport")
router.register("airplane-types", AirplaneTypeViewSet, basename="airplane-type")
router.register("airplanes", AirplaneViewSet, basename="airplane")
router.register("crews", CrewViewSet, basename="crew")
router.register("routes", RouteViewSet, basename="route")

urlpatterns = [
    path("", include(router.urls)),
]

app_name = "airport"
