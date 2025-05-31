from datetime import datetime

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny, IsAuthenticated
from airport.permissions import IsStaffUser, IsStaffOrOwner


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


@extend_schema(
    tags=["Country"],
    description="Retrieve list of countries or a single country by ID. "
                "Read-only access for all users; creation, update, deletion via admin panel only.",
)
class CountryViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    """
    Accessible for viewing by all users; editing,
    adding, and deleting are managed via the admin panel only.
    """

    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = (AllowAny,)


@extend_schema(
    tags=["City"],
    description="Retrieve list of cities or a single city by ID. "
                "Read-only access for all users; creation, update, deletion via admin panel only.",
)
class CityViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    """
    Accessible for viewing by all users; editing,
    adding, and deleting are managed via the admin panel only.
    """

    queryset = City.objects.select_related("country").all()
    serializer_class = CitySerializer
    permission_classes = (AllowAny,)


@extend_schema(
    tags=["Airport"],
    description="List and retrieve airports available for all users. "
                "Create, update, and delete allowed only for staff users.",
)
class AirportViewSet(viewsets.ModelViewSet):
    """
    List and retrieve allowed for any user.
    Create, update, delete allowed only for staff users.
    """

    queryset = Airport.objects.select_related("city").all()
    serializer_class = AirportSerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]
        return [IsStaffUser()]


@extend_schema(
    tags=["AirplaneType"],
    description="List and retrieve airplane types for all users. "
                "Create, update, and delete allowed only for staff users.",
)
class AirplaneTypeViewSet(viewsets.ModelViewSet):
    """
    List and retrieve allowed for any user.
    Create, update, delete allowed only for staff users.
    """

    queryset = AirplaneType.objects.all()
    serializer_class = AirplaneTypeSerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]
        return [IsStaffUser()]


@extend_schema(
    tags=["Airplane"],
    description="List and retrieve airplanes for all users. "
                "Create, update, and delete allowed only for staff users.",
)
class AirplaneViewSet(viewsets.ModelViewSet):
    """
    List and retrieve allowed for any user.
    Create, update, delete allowed only for staff users.
    """

    queryset = Airplane.objects.select_related("airplane_type").all()
    serializer_class = AirplaneSerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]
        return [IsStaffUser()]


@extend_schema(
    tags=["Crew"],
    description="List and retrieve crew members for all users. "
                "Create, update, and delete allowed only for staff users.",
)
class CrewViewSet(viewsets.ModelViewSet):
    """
    List and retrieve allowed for any user.
    Create, update, delete allowed only for staff users.
    """

    queryset = Crew.objects.all()
    serializer_class = CrewSerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]
        return [IsStaffUser()]


@extend_schema(
    tags=["Route"],
    description="List and retrieve routes for all users. "
                "Create, update, and delete allowed only for staff users.",
)
class RouteViewSet(viewsets.ModelViewSet):
    """
    List and retrieve allowed for any user.
    Create, update, delete allowed only for staff users.
    """

    queryset = Route.objects.select_related("source", "destination").all()
    serializer_class = RouteSerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]
        return [IsStaffUser()]


@extend_schema(
    tags=["Flight"],
    description="List and retrieve flights for all users. "
                "Create, update, and delete allowed only for staff users.",
)
class FlightViewSet(viewsets.ModelViewSet):
    """
    List and retrieve allowed for any user.
    Create, update, delete allowed only for staff users.
    """

    queryset = Flight.objects.all().select_related(
        "route",
        "airplane"
    ).prefetch_related("crew")
    serializer_class = FlightSerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]
        return [IsStaffUser()]

    def get_queryset(self):
        queryset = self.queryset
        route_id = self.request.query_params.get("route")
        airplane_id = self.request.query_params.get("airplane")
        departure_after = self.request.query_params.get("departure_after")
        departure_before = self.request.query_params.get("departure_before")

        if route_id:
            try:
                route_id = int(route_id)
                queryset = queryset.filter(route_id=route_id)
            except ValueError:
                pass

        if airplane_id:
            try:
                airplane_id = int(airplane_id)
                queryset = queryset.filter(airplane_id=airplane_id)
            except ValueError:
                pass

        if departure_after:
            try:
                departure_after_date = datetime.strptime(departure_after, "%Y-%m-%d")
                queryset = queryset.filter(departure_time__gte=departure_after_date)
            except ValueError:
                pass

        if departure_before:
            try:
                departure_before_date = datetime.strptime(departure_before, "%Y-%m-%d")
                queryset = queryset.filter(departure_time__lte=departure_before_date)
            except ValueError:
                pass

        return queryset

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "route",
                OpenApiTypes.INT,
                description="Filter flights by route ID (ex. ?route=3)",
                required=False,
            ),
            OpenApiParameter(
                "airplane",
                OpenApiTypes.INT,
                description="Filter flights by airplane ID (ex. ?airplane=5)",
                required=False,
            ),
            OpenApiParameter(
                "departure_after",
                OpenApiTypes.DATE,
                description="Filter flights with departure time on or after the date (YYYY-MM-DD)",
                required=False,
            ),
            OpenApiParameter(
                "departure_before",
                OpenApiTypes.DATE,
                description="Filter flights with departure time on or before the date (YYYY-MM-DD)",
                required=False,
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


@extend_schema(
    tags=["Order"],
    description="List orders for authenticated users. Users can only see their own orders. "
                "Order creation is allowed for authenticated users.",
    # Define different serializers for list and create actions
    request=OrderSerializer,
    responses={200: OrderListSerializer},
)
class OrderViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    """
    List and create orders only for authenticated users.
    Each user can only see their own orders.
    """

    permission_classes = [IsAuthenticated, IsStaffOrOwner]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related("tickets__flight")

    def get_serializer_class(self):
        if self.action == "list":
            return OrderListSerializer
        return OrderSerializer
