# Travel-Booking-System
The Travel Booking Application is a Django-based system for booking flights, trains, and buses. It supports user registration, automatic seat assignment, booking confirmation, and admin management, ensuring a smooth and organized travel experience.   2/2         Ask ChatGPT
# Travel Booking Application 
This is a Django-based web application for booking travel tickets (Flight, Train, and Bus), inspired by systems like IRCTC. The app supports user registration, login, search, booking, passenger details, and ticket generation, along with a powerful admin dashboard for managing travel options and bookings.

---

###  User Side
- User Registration & Login
- Search for travel options (Flight, Train, Bus) by source, destination, and date
- View travel details and available seats
- Book tickets by entering passenger information (Name, Age, Gender)
- Auto-generation of booking code and ticket
- View current and past bookings
- Cancel bookings and restore seat availability

### Admin Side
- Admin Login (default: `admin / admin@123`)
- Add/Edit/Delete:
  - Flights
  - Trains
  - Buses
- View and manage:
  - All bookings (Confirm/Cancel)
  - Registered users and their bookings
  - Seat availability for all travel options

---


---

## Models

### Travel Options
- **Flight, Train, Bus** (Separate models)
  - Fields: `travel_id`, `name`, `source`, `destination`, `departure`, `arrival`, `total_seats`, `available_seats`, `price_per_seat`

### Booking
- `booking_id`, `booking_code`, `user`, `travel_type`, `travel_flight/train/bus`, `booking_date`, `number_of_seats`, `total_price`, `status`

### Passenger
- `passenger_id`, `booking`, `name`, `age`, `gender`

### User
- `full_name`, `username`, `password`, `phone`, `aadhaar`, `address`

---

##  How to Run

1 click the run manage code
2. Install Dependencies
3. Apply Migrations
python manage.py makemigrations
python manage.py migrate
4.python manage.py createsuperuser # for admin login
5.run sample data 
6. Run the Server
python manage.py runserver or run.bat

Backend:
1.	User Management:
○	Implement user registration, login, and logout using Django's built-in authentication system.
○	Allow users to update their profile information.
2.	Travel Options:
○	Create a model for Travel Options (e.g., flight, train, bus), which includes fields such as:
■	Travel ID
■	Type (Flight, Train, Bus)
■	Source
■	Destination
■	Date and Time
■	Price
■	Available Seats
3.	Booking:
○	Allow users to book travel options by selecting a travel option, entering details, and confirming the booking.
○	Each booking should be stored in a Booking model, which includes:
■	Booking ID
■	User (Foreign Key)
■	Travel Option (Foreign Key)
■	Number of Seats
■	Total Price
■	Booking Date
■	Status (Confirmed, Cancelled)
4.	View and Manage Bookings:
○	Users should be able to view their current and past bookings.
○	Implement functionality to allow users to cancel bookings.

