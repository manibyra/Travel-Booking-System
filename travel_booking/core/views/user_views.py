from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from datetime import datetime

from core.models.flight import Flight
from core.models.train import Train
from core.models.bus import Bus
from core.models.booking import Booking
from core.models.passenger import Passenger
from core.forms import LoginForm

User = get_user_model()


# ---------------------- HOME ----------------------
def home(request):
    return render(request, 'home.html')


# ---------------------- REGISTER ----------------------
def register(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        username = request.POST.get('username')
        phone = request.POST.get('phone')
        aadhaar = request.POST.get('aadhaar')
        address = request.POST.get('address')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if not all([full_name, username, phone, aadhaar, address, password, confirm_password]):
            messages.error(request, "All fields are required.")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
            return redirect('register')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('register')

        user = User.objects.create_user(
            username=username,
            password=password,
            full_name=full_name,
            phone=phone,
            aadhaar=aadhaar,
            address=address
        )
        messages.success(request, 'Registration successful. Please log in.')
        return redirect('login')

    return render(request, 'user/register.html')


# ---------------------- LOGIN ----------------------
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user:
                login(request, user)
                if user.is_superuser:
                    return redirect('admin_dashboard')
                return redirect('user_dashboard')
            else:
                messages.error(request, 'Invalid credentials')
    else:
        form = LoginForm()
    return render(request, 'user/login.html', {'form': form})


# ---------------------- LOGOUT ----------------------
@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


# ---------------------- USER DASHBOARD ----------------------
@login_required
def user_dashboard(request):
    return render(request, 'user/user_dashboard.html')


# ---------------------- SEARCH TRAVEL ----------------------
@login_required
def search_travel(request):
    travel_type = request.GET.get('travel_type')
    source = request.GET.get('source')
    destination = request.GET.get('destination')
    travel_date = request.GET.get('travel_date')

    context = {
        'results': [],
        'search_done': False,
        'travel_type': travel_type,
        'source': source,
        'destination': destination,
        'travel_date': travel_date,
    }

    if travel_type and source and destination:
        source = source.lower()
        destination = destination.lower()
        travel_date_filter = {}

        if travel_date:
            travel_date_filter = {'departure_time__date': travel_date}

        if travel_type == 'flight':
            results = Flight.objects.filter(source__iexact=source, destination__iexact=destination, **travel_date_filter)
        elif travel_type == 'train':
            results = Train.objects.filter(source__iexact=source, destination__iexact=destination, **travel_date_filter)
        elif travel_type == 'bus':
            results = Bus.objects.filter(source__iexact=source, destination__iexact=destination, **travel_date_filter)
        else:
            results = []

        context['results'] = results
        context['search_done'] = True

    return render(request, 'user/search.html', context)


# ---------------------- BOOK TRAVEL ----------------------
@login_required
def book_travel(request, travel_type, travel_id):
    model_map = {'flight': Flight, 'train': Train, 'bus': Bus}
    travel_model = model_map.get(travel_type)

    if not travel_model:
        messages.error(request, "Invalid travel type.")
        return redirect('search_travel')

    travel = get_object_or_404(travel_model, pk=travel_id)

    if request.method == 'POST':
        seats = int(request.POST.get('seats'))

        if travel.available_seats < seats:
            messages.error(request, 'Not enough seats available.')
            return redirect('search_travel')

        booking_data = {
            'user': request.user,
            'travel_type': travel_type,
            'number_of_seats': seats,
            'total_price': travel.price * seats,
            'status': 'Pending'
        }

        if travel_type == 'flight':
            booking_data['travel_flight'] = travel
        elif travel_type == 'train':
            booking_data['travel_train'] = travel
        elif travel_type == 'bus':
            booking_data['travel_bus'] = travel

        booking = Booking.objects.create(**booking_data)
        booking.save()
        # Update seat availability
        travel.available_seats -= seats
        travel.save()

        return redirect('passenger_details', booking_id=booking.booking_id)


    return render(request, 'user/book.html', {
        'travel': travel,
        'travel_type': travel_type
    })


@login_required
def passenger_details(request, booking_id):
    booking = get_object_or_404(Booking, booking_id=booking_id, user=request.user)

    if request.method == 'POST':
        # 1️⃣ pick the travel object for seat‑count reference
        travel = (
            booking.travel_flight if booking.travel_type == 'flight' else
            booking.travel_train  if booking.travel_type == 'train'  else
            booking.travel_bus
        )

        # 2️⃣ seats already taken on the same flight/train/bus & confirmed
        taken = Passenger.objects.filter(
            booking__travel_type=booking.travel_type,
            booking__status='Confirmed',
            **{f'booking__travel_{booking.travel_type}': travel}
        ).values_list('seat_number', flat=True)

        # 3️⃣ build the full seat list (S1, S2, …)
        all_seats = [f"S{i}" for i in range(1, travel.total_seats + 1)]
        available = [s for s in all_seats if s not in taken]

        if len(available) < booking.number_of_seats:
            messages.error(request, 'Not enough seats available.')
            return redirect('search_travel')

        # first N free seats become ours
        seat_pool = available[:booking.number_of_seats]

        # 4️⃣ save each passenger with an auto seat number
        for idx in range(booking.number_of_seats):
            name   = request.POST.get(f'name_{idx}')
            age    = request.POST.get(f'age_{idx}')
            gender = request.POST.get(f'gender_{idx}')

            if name and age and gender:
                Passenger.objects.create(
                    booking     = booking,
                    name        = name,
                    age         = int(age),
                    gender      = gender,
                    seat_number = seat_pool[idx]       # ← auto‑assigned
                )

        booking.status = 'Confirmed'
        booking.save()

        return redirect('ticket', booking_id=booking.booking_id)

    # GET‑request: render the form
    seat_range = range(booking.number_of_seats)
    return render(request, 'user/passenger_details.html', {
        'booking'    : booking,
        'seat_range' : seat_range,          # used for looping inputs
        'seat_count' : booking.number_of_seats,
    })


# ---------------------- MY BOOKINGS ----------------------
@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-booking_date')
    return render(request, 'user/my_bookings.html', {'bookings': bookings})


# ---------------------- CANCEL BOOKING ----------------------
@login_required
@transaction.atomic
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, booking_id=booking_id, user=request.user)
   
    if booking.status != 'Cancelled':
        travel = None
        if booking.travel_type == 'flight':
            travel = booking.travel_flight
        elif booking.travel_type == 'train':
            travel = booking.travel_train
        elif booking.travel_type == 'bus':
            travel = booking.travel_bus

        if travel:
            travel.available_seats += booking.number_of_seats
            travel.save()

        booking.status = 'Cancelled'
        booking.save()

    return redirect('my_bookings')


# ---------------------- CANCEL BOOKING CONFIRM ----------------------
@login_required
def cancel_booking_confirm(request, booking_id):
    booking = get_object_or_404(Booking, booking_id=booking_id, user=request.user)
    return render(request, 'user/cancel_confirm.html', {'booking': booking})


# ---------------------- FALLBACK CANCEL ----------------------
@csrf_exempt
@login_required
def cancel_booking_fallback(request):
    if request.method == "POST":
        booking_code = request.POST.get('booking_code')
        booking = Booking.objects.filter(booking_code=booking_code, user=request.user).first()
        if booking:
            booking.status = 'Cancelled'
            booking.save()
            # Restore seats if needed
    return redirect('my_bookings')

@login_required
def ticket_view(request, booking_id):
    booking = get_object_or_404(Booking, booking_id=booking_id, user=request.user)
    passengers = booking.passengers.all()

    # Detect the travel model based on type
    travel = None
    if booking.travel_type == 'flight':
        travel = booking.travel_flight
    elif booking.travel_type == 'train':
        travel = booking.travel_train
    elif booking.travel_type == 'bus':
        travel = booking.travel_bus

    context = {
        'booking': booking,
        'travel': travel,
        'passengers': passengers,
    }
    return render(request, 'user/ticket.html', context)

