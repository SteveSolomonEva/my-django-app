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
def book_service(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data

            # Validate times
            if cd['end_time'] <= cd['start_time']:
                return render(request, 'booking_form.html', {
                    'form': form,
                    'error': 'End time must be after start time.'
                })

            # Save booking
            Booking.objects.create(
                full_name=cd['full_name'],
                email=cd['email'],
                phone=cd['phone'],
                date=cd['date'],
                start_time=cd['start_time'],
                end_time=cd['end_time'],
                status='confirmed'
            )
            return redirect('booking_success')
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
