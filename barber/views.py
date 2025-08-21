from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

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

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Booking, Service
from .forms import BookingForm

@login_required
def book_service(request):
    services = Service.objects.all()  # fetch all services to show in the form

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data

            # Field-level sanity check
            if cd['end_time'] <= cd['start_time']:
                form.add_error('end_time', 'End time must be after start time.')
            else:
                # Overlap check: any confirmed booking that intersects this window on this date
                overlap_exists = Booking.objects.filter(
                    date=cd['date'],
                    status='confirmed'
                ).filter(
                    Q(start_time__lt=cd['end_time']) &
                    Q(end_time__gt=cd['start_time'])
                ).exists()

                if overlap_exists:
                    form.add_error(None, 'That time slot is already taken. Please choose another one.')
                else:
                    # Assign the selected service
                    service_id = request.POST.get('service')
                    if not service_id:
                        form.add_error('service', 'Please select a service.')
                        return render(request, 'booking_form.html', {'form': form, 'services': services})

                    service = Service.objects.get(id=int(service_id))

                    booking = Booking.objects.create(
                        full_name=cd['full_name'],
                        email=cd['email'],
                        phone=cd['phone'],
                        date=cd['date'],
                        start_time=cd['start_time'],
                        end_time=cd['end_time'],
                        status='confirmed',
                        service=service
                    )
                    return redirect('booking_success', booking_id=booking.id)
    else:
        form = BookingForm()

    return render(request, 'booking_form.html', {'form': form, 'services': services})



# Booking success page
def booking_success(request, booking_id):
    # Get the booking object or return 404 if not found
    booking = get_object_or_404(Booking, id=booking_id)
    
    return render(request, 'booking_success.html', {'booking': booking})



# Authentication
class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    success_url = reverse_lazy('bookings')


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')
