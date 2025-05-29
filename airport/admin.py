from django.contrib import admin

from .models import (
    Airport,
    Crew,
    AirplaneType,
    Airplane,
    Route,
    Flight,
    Ticket,
    City,
    Country,
    Order,
)


admin.site.register(Crew)
admin.site.register(AirplaneType)
admin.site.register(Airplane)
admin.site.register(Order)
admin.site.register(Country)
admin.site.register(City)
admin.site.register(Airport)
admin.site.register(Route)
admin.site.register(Flight)
admin.site.register(Ticket)


