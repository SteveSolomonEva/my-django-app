from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['full_name', 'email', 'phone', 'date', 'start_time', 'end_time']
        labels = {
            'full_name': 'Your Full Name',
            'email': 'Email Address',
            'phone': 'Phone Number',
            'date': 'Booking Date',
            'start_time': 'Start Time',
            'end_time': 'End Time',
        }
        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': 'Enter your full name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter your email'}),
            'phone': forms.TextInput(attrs={'placeholder': '08158216178'}),
            'date': forms.DateInput(attrs={'type': 'date', 'placeholder': 'Select a date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time', 'placeholder': 'When your booking starts'}),
            'end_time': forms.TimeInput(attrs={'type': 'time', 'placeholder': 'When your booking ends'}),
        }
