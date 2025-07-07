from django.db import models
from core.models.booking import Booking

class Passenger(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='passengers')
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    seat_number = models.CharField(max_length=10)
    class Meta:
        unique_together = ('seat_number', 'booking')
    def __str__(self):
        return f"{self.name} - Seat: {self.seat_number} (Booking ID: {self.booking.booking_id})"

