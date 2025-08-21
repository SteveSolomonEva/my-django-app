from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required

from .models import Booking, Service
from .forms import BookingForm


# Home & About
class HomePageView(TemplateView):
    template_name = 'home.html'


class AboutPageView(TemplateView):
    template_name = 'about.html'

def bookings_list(request):
    # Show all bookings
    bookings = Booking.objects.all()
    return render(request, 'bookings.html', {'bookings': bookings})

@login_required
def my_booking(request):
    # Show only bookings for the logged-in user
    bookings = Booking.objects.filter(email=request.user.email)
    return render(request, 'bookings.html', {'bookings': bookings})

def services_list(request):
    services = Service.objects.all()
    return render(request, 'services.html', {'services': services})

def all_services(request):
    serves = Service.objects.all()
    return render(request, 'our_services.html', {'bookings': serves})

def gallery(request):
    pictures = Service.objects.all()
    return render(request, 'gallery.html', {'bookings': pictures})

# Booking creation page
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db.models import Q
from .forms import BookingForm
from .models import Booking

@login_required
def book_service(request):
    if not request.user.is_authenticated:   # 👈 added check
        return redirect('signup')           # or 'login'

    if request.method == 'POST':            # 👈 your original code continues here
        form = BookingForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data

            # Field-level sanity check
            if cd['end_time'] <= cd['start_time']:
                # attach to the field so the error shows nicely under it
                form.add_error('end_time', 'End time must be after start time.')
            else:
                # Overlap check (basic): any confirmed booking that intersects this window on this date
                overlap_exists = Booking.objects.filter(
                    date=cd['date'],
                    status='confirmed'  # adjust if your model uses a different status value
                ).filter(
                    Q(start_time__lt=cd['end_time']) &
                    Q(end_time__gt=cd['start_time'])
                ).exists()

                if overlap_exists:
                    # non-field error (top of form), since it concerns multiple fields
                    form.add_error(None, 'That time slot is already taken. Please choose another one.')
                else:
                    booking = Booking.objects.create(
                        full_name=cd['full_name'],
                        email=cd['email'],
                        phone=cd['phone'],
                        date=cd['date'],
                        start_time=cd['start_time'],
                        end_time=cd['end_time'],
                        status='confirmed'
                    )
                    # Redirect with ID so success page can show details if you want
                    return redirect('booking_success', booking_id=booking.id)
        # if invalid, fall through to re-render with errors
    else:
        form = BookingForm()

    return render(request, 'booking_form.html', {'form': form})


# Booking success page
def booking_success(request):
    return render(request, 'booking_success.html')


# Authentication
class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    success_url = reverse_lazy('bookings')


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')
