from django.contrib import admin

# Register your models here.

from .models import Service, Booking

admin.site.register(Service)
admin.site.register(Booking)



class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'image')  # show in list view
    fields = ('name', 'description', 'price', 'image')  # show in edit view
