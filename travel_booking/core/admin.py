#core/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models.flight import Flight
from .models.train import Train
from .models.bus import Bus
from .models.booking import Booking
from .models.passenger import Passenger
from .models.user import CustomUser

@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = ('travel_id', 'name', 'source', 'destination', 'departure_time', 'arrival_time', 'available_seats', 'price')
    search_fields = ('source', 'destination', 'name')
    list_filter = ('source', 'destination')

@admin.register(Train)
class TrainAdmin(admin.ModelAdmin):
    list_display = ('travel_id', 'name', 'source', 'destination', 'departure_time', 'arrival_time', 'available_seats', 'price')
    search_fields = ('source', 'destination', 'name')
    list_filter = ('source', 'destination')

@admin.register(Bus)
class BusAdmin(admin.ModelAdmin):
    list_display = ('travel_id', 'name', 'source', 'destination', 'departure_time', 'arrival_time', 'available_seats', 'price')
    search_fields = ('source', 'destination', 'name')
    list_filter = ('source', 'destination')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('booking_id', 'user', 'travel_type', 'booking_date', 'number_of_seats', 'total_price', 'status')
    date_hierarchy = 'booking_date'
    search_fields = ('user__username', 'travel_type')
    list_filter = ('status', 'travel_type')

@admin.register(Passenger)
class PassengerAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'gender', 'booking')


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'full_name', 'phone', 'aadhaar', 'address')
