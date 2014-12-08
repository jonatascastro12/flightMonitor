from django.contrib import admin
from monitor.models import FilterAlert, FilterAlertAdmin, Flight, FlightAdmin
# Register your models here.

admin.site.register(Flight,FlightAdmin)
admin.site.register(FilterAlert,FilterAlertAdmin)
