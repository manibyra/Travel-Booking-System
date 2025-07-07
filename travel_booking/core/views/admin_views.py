from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from core.models.flight import Flight
from core.models.train import Train
from core.models.bus import Bus
from core.models.booking import Booking
from core.models.passenger import Passenger
from django.contrib.auth.models import User

def admin_required(view_func):
    return user_passes_test(lambda u: u.is_superuser)(view_func)

@admin_required
def admin_dashboard(request):
    flights = Flight.objects.count()
    trains = Train.objects.count()
    buses = Bus.objects.count()
    bookings = Booking.objects.count()
    users = User.objects.filter(is_superuser=False).count()
    return render(request, 'admin/dashboard.html', {
        'flight_count': flights,
        'train_count': trains,
        'bus_count': buses,
        'booking_count': bookings,
        'user_count': users,
    })

# FLIGHT MANAGEMENT
@admin_required
def manage_flights(request):
    flights = Flight.objects.all()
    return render(request, 'admin/manage_flights.html', {'flights': flights})

@admin_required
def add_flight(request):
    if request.method == 'POST':
        Flight.objects.create(
            name=request.POST['name'],
            source=request.POST['source'],
            destination=request.POST['destination'],
            departure_time=request.POST['departure_time'],
            arrival_time=request.POST['arrival_time'],
            total_seats=request.POST['total_seats'],
            available_seats=request.POST['total_seats'],
            price=request.POST['price']
        )
        messages.success(request, 'Flight added successfully.')
        return redirect('manage_flights')
    return render(request, 'admin/add_flight.html')

@admin_required
def delete_flight(request, flight_id):
    flight = get_object_or_404(Flight, id=flight_id)
    flight.delete()
    messages.success(request, 'Flight deleted successfully.')
    return redirect('manage_flights')

# TRAIN MANAGEMENT
@admin_required
def manage_trains(request):
    trains = Train.objects.all()
    return render(request, 'admin/manage_trains.html', {'trains': trains})

@admin_required
def add_train(request):
    if request.method == 'POST':
        Train.objects.create(
            name=request.POST['name'],
            source=request.POST['source'],
            destination=request.POST['destination'],
            departure_time=request.POST['departure_time'],
            arrival_time=request.POST['arrival_time'],
            total_seats=request.POST['total_seats'],
            available_seats=request.POST['total_seats'],
            price=request.POST['price']
        )
        messages.success(request, 'Train added successfully.')
        return redirect('manage_trains')
    return render(request, 'admin/add_train.html')

@admin_required
def delete_train(request, train_id):
    train = get_object_or_404(Train, id=train_id)
    train.delete()
    messages.success(request, 'Train deleted successfully.')
    return redirect('manage_trains')

# BUS MANAGEMENT
@admin_required
def manage_buses(request):
    buses = Bus.objects.all()
    return render(request, 'admin/manage_buses.html', {'buses': buses})

@admin_required
def add_bus(request):
    if request.method == 'POST':
        Bus.objects.create(
            name=request.POST['name'],
            source=request.POST['source'],
            destination=request.POST['destination'],
            departure_time=request.POST['departure_time'],
            arrival_time=request.POST['arrival_time'],
            total_seats=request.POST['total_seats'],
            available_seats=request.POST['total_seats'],
            price=request.POST['price']
        )
        messages.success(request, 'Bus added successfully.')
        return redirect('manage_buses')
    return render(request, 'admin/add_bus.html')

@admin_required
def delete_bus(request, bus_id):
    bus = get_object_or_404(Bus, id=bus_id)
    bus.delete()
    messages.success(request, 'Bus deleted successfully.')
    return redirect('manage_buses')

# BOOKING MANAGEMENT
@admin_required
def view_all_bookings(request):
    bookings = Booking.objects.all().order_by('-booking_date')
    return render(request, 'admin/view_all_bookings.html', {'bookings': bookings})

@admin_required
def change_booking_status(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    if request.method == 'POST':
        booking.status = request.POST.get('status')
        booking.save()
        messages.success(request, 'Booking status updated.')
        return redirect('view_all_bookings')
    return render(request, 'admin/change_booking_status.html', {'booking': booking})

# USER MANAGEMENT
@admin_required
def manage_users(request):
    users = User.objects.filter(is_superuser=False)
    return render(request, 'admin/manage_users.html', {'users': users})

@staff_member_required
def admin_cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, booking_id=booking_id)

    if booking.status != 'Cancelled':
        if booking.travel_type == 'Flight' and booking.travel_flight:
            travel = booking.travel_flight
        elif booking.travel_type == 'Train' and booking.travel_train:
            travel = booking.travel_train
        elif booking.travel_type == 'Bus' and booking.travel_bus:
            travel = booking.travel_bus
        else:
            return redirect('admin_manage_bookings')

        travel.available_seats += booking.number_of_seats
        travel.save()

        booking.status = 'Cancelled'
        booking.save()
        messages.success(request, f"Booking #{booking.booking_id} cancelled successfully.")

    return redirect('admin_manage_bookings')
