# -*- coding: utf-8 -*-

from django.core.mail import send_mail
from monitor.models import Flight, FilterAlert, WEEKDAY
from monitor.serializers import FlightSerializer
from rest_framework import generics
import logging
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
import math


logger = logging.getLogger(__name__)
alerts = FilterAlert.objects.filter(active=True)


def updateAlerts():
    alerts = FilterAlert.objects.filter(active=True)
    return HttpResponse("OK")


class ExtentListCreateAPIView(generics.ListCreateAPIView):
    """
    Concrete view for listing a queryset or creating a model instance.
    """

    def post(self, request, *args, **kwargs):
        flight_s = FlightSerializer(data=request.data)
        filter_date = True
        filter_price = True
        filter_destination = True
        filter_weekday = True
        filter_destination_except = True
        if (flight_s.is_valid()):
            for alert in alerts:
                if flight_s.validated_data.get('price') <= alert.maxPrice:
                    filter_price = True
                if alert.dateStart and alert.dateEnd:
                    filter_date = False
                    if flight_s.validated_data.get('departDate') >= alert.dateStart and flight_s.validated_data.get(
                            'departDate') <= alert.dateEnd:
                        filter_date = True
                if alert.destinationFilter:
                    filter_destination = False
                    if flight_s.validated_data.get('destination') == alert.destinationFilter:
                        filter_destination = True
                if alert.weekday:
                    filter_weekday = False
                    days_of_week = [int(math.log(i, 2)) for i in WEEKDAY.get_selected_values(alert.weekday)]

                    if flight_s.validated_data.get('departDate').weekday() in days_of_week:
                        filter_weekday = True
                if alert.destinationExcept:
                    filter_destination_except = False
                    if "," in alert.destinationExcept:
                        destinations = alert.destinationExcept.split(",")
                        if flight_s.validated_data.get('destination') not in destinations:
                            filter_destination_except = True
                    elif flight_s.validated_data.get('destination').strip() == alert.destinationExcept.strip():
                        filter_destination_except = True

                if filter_date and filter_price and filter_destination and filter_weekday and filter_destination_except:
                    send_mail(
                        "Alerta de preço de passagem: ".decode('utf8') + flight_s.validated_data.get('destination'),
                        "PREÇO: ".decode('utf8') + str(
                            flight_s.validated_data.get('price')) + "\n" + flight_s.validated_data.get('searchUrl') + "\n" +
                            str(flight_s.validated_data.get('departDate')),
                        'sistema@passagens.com.br', [alert.email])

            if flight_s.validated_data.get('price') < 2000:
                return self.create(request, *args, **kwargs)
            return Response({"message": "Price higher than 2000.00"}, status=status.HTTP_202_ACCEPTED)


# Create your views here.
class FlightList(ExtentListCreateAPIView):
    queryset = Flight.objects.all()[:50]
    serializer_class = FlightSerializer


class FlightDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
