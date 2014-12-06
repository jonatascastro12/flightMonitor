from django.db import models
from django.contrib import admin

# Create your models here.
class Flight(models.Model):
	departDate = models.DateField()
	returnDate = models.DateField()
	origin = models.CharField(max_length=250)
	destination = models.CharField(max_length=250)
	searchUrl = models.CharField(max_length=600)
	price = models.DecimalField(max_digits=6, decimal_places=2)
	timestamp =  models.DateTimeField(auto_now_add=True, blank=True)

class FlightAdmin(admin.ModelAdmin):
	list_display = ('departDate','returnDate','destination','price','timestamp')
	list_filter = ['destination', 'departDate']
