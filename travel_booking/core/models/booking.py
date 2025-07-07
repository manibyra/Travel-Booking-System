from django.db import models
from django.conf import settings
from core.models.flight import Flight
from core.models.train import Train
from core.models.bus import Bus
from django.core.exceptions import ValidationError
import uuid

class Booking(models.Model):
    TRAVEL_TYPE_CHOICES = [
        ('flight', 'Flight'),
        ('train', 'Train'),
        ('bus', 'Bus'),
    ]

    STATUS_CHOICES = [
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled'),
    ]
    booking_id = models.AutoField(primary_key=True)
    booking_code = models.CharField(max_length=20, unique=True, db_index=True, blank=True)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    travel_type = models.CharField(max_length=10, choices=TRAVEL_TYPE_CHOICES)

    travel_flight = models.ForeignKey(Flight, null=True, blank=True, on_delete=models.SET_NULL)
    travel_train = models.ForeignKey(Train, null=True, blank=True, on_delete=models.SET_NULL)
    travel_bus = models.ForeignKey(Bus, null=True, blank=True, on_delete=models.SET_NULL)

    booking_date = models.DateTimeField(auto_now_add=True)
    number_of_seats = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Confirmed')

    def __str__(self):
        travel = self.get_travel_option()
        travel_name = travel.name if travel else "N/A"
        return f"{self.booking_code} - {self.travel_type.title()} - {travel_name}"

    def get_travel_option(self):
        if self.travel_type == 'flight':
            return self.travel_flight
        elif self.travel_type == 'train':
            return self.travel_train
        elif self.travel_type == 'bus':
            return self.travel_bus
        return None

    def get_travel_id(self):
        travel = self.get_travel_option()
        return travel.travel_id if travel else None

    def get_travel_name(self):
        travel = self.get_travel_option()
        return travel.name if travel else None

    def clean(self):
        super().clean()
        if self.travel_type == 'flight' and not self.travel_flight:
            raise ValidationError("Flight must be selected for travel type 'flight'.")
        elif self.travel_type == 'train' and not self.travel_train:
            raise ValidationError("Train must be selected for travel type 'train'.")
        elif self.travel_type == 'bus' and not self.travel_bus:
            raise ValidationError("Bus must be selected for travel type 'bus'.")

    def save(self, *args, **kwargs):
        if not self.booking_code:
            self.booking_code = f"BK{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    class Meta:
        indexes = [
            models.Index(fields=['booking_code']),
        ]