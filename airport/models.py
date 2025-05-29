from django.db import models

from config import settings


# Екіпаж
class Crew(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


# Тип літака
class AirplaneType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"


# Літаки
class Airplane(models.Model):
    name = models.CharField(max_length=255)
    rows = models.IntegerField()
    seats_in_rows = models.IntegerField()
    airplane_type = models.ForeignKey(AirplaneType, on_delete=models.CASCADE, related_name="airplane_type")

    def __str__(self):
        return f"{self.name}"


# Ордер
class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders")

    def __str__(self):
        return f"{self.created_at}"


# Країна
class Country(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

# Місто
class City(models.Model):
    name = models.CharField(max_length=255)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="cities")

    def __str__(self):
        return f"{self.name}, {self.country}"


# Аеропорт
class Airport(models.Model):
    name = models.CharField(max_length=255)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name="airports")

    def __str__(self):
        return f"{self.name}"


# Маршрут
class Route(models.Model):
    source = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="routes")
    destination = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="routes")
    distance = models.IntegerField()

    def __str__(self):
        return f"{self.source} -> {self.destination}"


# Політ
class Flight(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name="flights")
    airplane = models.ForeignKey(Airplane, on_delete=models.CASCADE, related_name="flights")
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    crew = models.ManyToManyField(Crew)


# Квитки
class Ticket(models.Model):
    row_number = models.IntegerField()
    seat_number = models.IntegerField()
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name="tickets")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="tickets")

    class Meta:
        unique_together = ("row_number", "seat_number", "flight")

    def __str__(self):
        return f"{self.order}"