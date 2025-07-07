from django.urls import path
from . import views
from core.views.user_views import cancel_booking_fallback
from core.views import user_views, admin_views
from core.views.user_views import passenger_details
urlpatterns = [
    # User URLs
    path('', user_views.home, name='home'),
    path('register/', user_views.register, name='register'),
    path('login/', user_views.login_view, name='login'),
    path('logout/', user_views.logout_view, name='logout'),
    path('dashboard/', user_views.user_dashboard, name='user_dashboard'),
    path('search/', user_views.search_travel, name='search_travel'),
    path('book/<str:travel_type>/<int:travel_id>/', user_views.book_travel, name='book_travel'),
    path('my_bookings/', user_views.my_bookings, name='my_bookings'),
    path('cancel/<int:booking_id>/confirm/', user_views.cancel_booking_confirm, name='cancel_booking_confirm'),
    path('cancel/<int:booking_id>/', user_views.cancel_booking, name='cancel_booking'),
    path('cancel_fallback/', cancel_booking_fallback, name='cancel_booking_fallback'),
    path('ticket/<int:booking_id>/', user_views.ticket_view, name='ticket'),
    path('passenger-details/<int:booking_id>/', passenger_details, name='passenger_details'),
    # Admin URLs
    path('admin/dashboard/', admin_views.admin_dashboard, name='admin_dashboard'),
    path('admin/flights/', admin_views.manage_flights, name='manage_flights'),
    path('admin/flights/add/', admin_views.add_flight, name='add_flight'),
    path('admin/flights/delete/<int:flight_id>/', admin_views.delete_flight, name='delete_flight'),
    path('admin/trains/', admin_views.manage_trains, name='manage_trains'),
    path('admin/trains/add/', admin_views.add_train, name='add_train'),
    path('admin/trains/delete/<int:train_id>/', admin_views.delete_train, name='delete_train'),
    path('admin/buses/', admin_views.manage_buses, name='manage_buses'),
    path('admin/buses/add/', admin_views.add_bus, name='add_bus'),
    path('admin/buses/delete/<int:bus_id>/', admin_views.delete_bus, name='delete_bus'),
    path('admin/bookings/', admin_views.view_all_bookings, name='view_all_bookings'),
    path('admin/bookings/status/<int:booking_id>/', admin_views.change_booking_status, name='change_booking_status'),
    path('admin/users/', admin_views.manage_users, name='manage_users'),
    
]
