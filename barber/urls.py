from django.urls import path
from .views import HomePageView, AboutPageView, CustomLoginView, SignUpView
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("about/", AboutPageView.as_view(), name="about"),
    path("login/", CustomLoginView.as_view(), name='login'),
    path("signup/", SignUpView.as_view(), name='signup'),
    path("logout/", LogoutView.as_view(next_page='/'), name='logout'),

    # Booking paths
    path("bookings/", views.bookings_list, name="bookings"),        # list all bookings
    path("book/", views.book_service, name="book_service"),          # create a new booking
    path("booking/success/", views.booking_success, name="booking_success"),
    path('services/', views.services_list, name='services'),
    path('our_service/', views.all_services, name='serves'),
    path('gallery/', views.gallery, name= 'pictures'),
    #path("bookings/", views.bookings_list, name="bookings"),  # all bookings
    path("my-booking/", views.my_booking, name="my_booking"), # personal bookings



]
