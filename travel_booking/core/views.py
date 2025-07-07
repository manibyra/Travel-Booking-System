from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import HttpResponse
from .models import Flight, Train, Bus, Booking, Passenger
from .forms import PassengerFormSet, SearchForm
from django.contrib.auth import authenticate, login, logout
from .models import User
from django.contrib.auth import get_user_model

User = get_user_model()

# ----------------- Home View -----------------
def home(request):
    return render(request, 'home.html')

# ----------------- User Registration -----------------
# ----------------- User Registration -----------------
def register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        username = request.POST.get('username')
        phone = request.POST.get('phone')
        aadhaar = request.POST.get('aadhaar')
        address = request.POST.get('address')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('register')

        user = User.objects.create_user(
            username=username,
            password=password,
            full_name=name,
            phone=phone,
            aadhaar=aadhaar,
            address=address,
        )
        messages.success(request, "Registration successful. Please log in.")
        return redirect('login')
    
    return render(request, 'user/register.html')

# ----------------- User Login -----------------
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid credentials.")
            return redirect('login')

    return render(request, 'user/login.html')


# ----------------- Logout -----------------
@login_required
def logout_view(request):
    logout(request)
    return redirect('home')


# ----------------- Dashboard -----------------
@login_required
def dashboard(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-booking_date')
    return render(request, 'user/dashboard.html', {'bookings': bookings})


# ----------------- Search Travel -----------------
@login_required
def search_travel(request):
    form = SearchForm(request.GET or None)
    results = []

    if form.is_valid():
        travel_type = form.cleaned_data['travel_type']
        source = form.cleaned_data['source']
        destination = form.cleaned_data['destination']
        date = form.cleaned_data['date']

        if travel_type == 'flight':
            results = Flight.objects.filter(source=source, destination=destination, date=date)
        elif travel_type == 'train':
            results = Train.objects.filter(source=source, destination=destination, date=date)
        elif travel_type == 'bus':
            results = Bus.objects.filter(source=source, destination=destination, date=date)

    return render(request, 'user/search.html', {'form': form, 'results': results})


# ----------------- Book Travel -----------------
@login_required
def book_travel(request, travel_type, travel_id):
    if travel_type == 'flight':
        travel = get_object_or_404(Flight, id=travel_id)
    elif travel_type == 'train':
        travel = get_object_or_404(Train, id=travel_id)
    else:
        travel = get_object_or_404(Bus, id=travel_id)

    formset = PassengerFormSet(request.POST or None)

    if request.method == 'POST' and formset.is_valid():
        num_seats = len(formset.cleaned_data)
        if travel.available_seats < num_seats:
            messages.error(request, "Not enough available seats.")
            return redirect('search_travel')

        booking = Booking.objects.create(
            user=request.user,
            travel_type=travel_type,
            travel_id=travel.id,
            number_of_seats=num_seats,
            total_price=num_seats * travel.price,
            booking_date=timezone.now(),
            status='Confirmed',
        )

        for passenger_form in formset:
            Passenger.objects.create(
                booking=booking,
                name=passenger_form['name'],
                age=passenger_form['age'],
                gender=passenger_form['gender']
            )

        travel.available_seats -= num_seats
        travel.save()

        messages.success(request, "Booking successful!")
        return redirect('dashboard')

    return render(request, 'user/book.html', {
        'travel': travel,
        'formset': formset,
        'travel_type': travel_type
    })


# ----------------- Cancel Booking -----------------
@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    if booking.status == 'Cancelled':
        messages.info(request, "Booking already cancelled.")
        return redirect('dashboard')

    travel = booking.get_travel_instance()
    travel.available_seats += booking.number_of_seats
    travel.save()

    booking.status = 'Cancelled'
    booking.save()
    messages.success(request, "Booking cancelled successfully.")
    return redirect('dashboard')

def cancel_booking_fallback(request):
    return HttpResponse("This is the fallback page for booking cancellation.")
