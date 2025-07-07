from django.db import models

class Flight(models.Model):
    travel_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)  # Airline Name
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    total_seats = models.IntegerField()
    available_seats = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name} ({self.travel_id})"
