from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from core.models.passenger import Passenger
from core.models.booking import Booking

CustomUser = get_user_model()

# User Registration Form
class UserRegisterForm(UserCreationForm):
    full_name = forms.CharField(max_length=100)
    phone = forms.CharField(max_length=10)
    aadhaar = forms.CharField(max_length=12)
    address = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = CustomUser
        fields = ['username', 'full_name', 'phone', 'aadhaar', 'address', 'password1', 'password2']

# Login Form
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

# Passenger Form
class PassengerForm(forms.ModelForm):
    class Meta:
        model = Passenger
        fields = ['name', 'age', 'gender']

# Booking Form
class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['travel_type', 'number_of_seats']

# Travel Search Form
class TravelSearchForm(forms.Form):
    TRAVEL_CHOICES = [
        ('flight', 'Flight'),
        ('train', 'Train'),
        ('bus', 'Bus'),
    ]
    travel_type = forms.ChoiceField(choices=TRAVEL_CHOICES)
    source = forms.CharField(max_length=100)
    destination = forms.CharField(max_length=100)
    date = forms.DateField(widget=forms.SelectDateWidget)
