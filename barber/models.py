from django.db import models

# Create your models here.

class Service(models.Model):
    name = models.CharField(max_length=112)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    image = models.ImageField(upload_to='services/', blank=True, null=True)
    
    def __str__(self):
        return self.name
    

class Booking(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=40)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField(default='12:00')

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("cancelled", "Cancelled"),
    ]

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='confirmed')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} → {self.service.name} on {self.date}"