import os
import django
from datetime import datetime, timedelta
import random

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "travel_booking.settings")
django.setup()

from core.models.bus import Bus
from core.models.train import Train
from core.models.flight import Flight

cities = ['Chennai', 'Hyderabad', 'Bangalore', 'Mumbai', 'Delhi', 'Kolkata', 'Pune', 'Ahmedabad', 'Jaipur', 'Guntur', 'Nellore', 'Vijayawada']

def create_entries(model, prefix, count):
    for i in range(1, count + 1):
        source, destination = random.sample(cities, 2)
        dep_time = datetime(2025, 7, random.randint(8, 28), random.randint(5, 22), 1)
        arr_time = dep_time + timedelta(hours=random.randint(2, 8))
        total_seats = random.randint(30, 60)
        available_seats = random.randint(20, total_seats)
        price = random.randint(500, 2000)
        model.objects.create(
            travel_id=f"{prefix}-{str(i).zfill(3)}",
            name=f"{prefix.capitalize()} Express {i}",
            source=source,
            destination=destination,
            departure_time=dep_time,
            arrival_time=arr_time,
            total_seats=total_seats,
            available_seats=available_seats,
            price=price   # ← corrected field name
        )

create_entries(Bus, "BUS", 30)
create_entries(Train, "TRAIN", 30)
create_entries(Flight, "FLIGHT", 20)

print("✅ Sample travel data inserted successfully.")
