from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from core.forms import UserRegisterForm, LoginForm
from django.contrib.auth.decorators import login_required

def user_register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.full_name = form.cleaned_data.get('full_name')
            user.profile.phone = form.cleaned_data.get('phone')
            user.profile.aadhaar = form.cleaned_data.get('aadhaar')
            user.profile.address = form.cleaned_data.get('address')
            user.save()
            messages.success(request, 'Registration successful. Please log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'user/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_superuser:
                    return redirect('admin_dashboard')
                return redirect('user_dashboard')
            else:
                messages.error(request, 'Invalid credentials')
    else:
        form = LoginForm()
    return render(request, 'user/login.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)
    return redirect('login')
