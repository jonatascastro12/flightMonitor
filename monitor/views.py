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


def updateAlerts(r):
    global alerts
    alerts = FilterAlert.objects.filter(active=True)
    return HttpResponse("OK")


class ExtentListCreateAPIView(generics.ListCreateAPIView):
    """
    Concrete view for listing a queryset or creating a model instance.
    """

    def post(self, request, *args, **kwargs):
        flight_s = FlightSerializer(data=request.data)

        if (flight_s.is_valid()):
            for alert in alerts:
                filter_permit = True
                if flight_s.validated_data.get('price') > alert.maxPrice:
                    filter_permit = False
                if alert.dateStart and alert.dateEnd:
                    if flight_s.validated_data.get('departDate') >= alert.dateStart or flight_s.validated_data.get(
                            'departDate') > alert.dateEnd:
                        filter_permit = False
                if alert.destinationFilter:
                    if flight_s.validated_data.get('destination').strip() != alert.destinationFilter.strip():
                        filter_permit = False
                if alert.weekday:
                    days_of_week = [int(math.log(i, 2)) for i in WEEKDAY.get_selected_values(alert.weekday)]
                    if flight_s.validated_data.get('departDate').weekday() not in days_of_week:
                        filter_permit = False
                if alert.destinationExcept:
                    if "," in alert.destinationExcept:
                        excepts = alert.destinationExcept.split(",")
                        excepts = [str(e).strip() for e in excepts]
                        if flight_s.validated_data.get('destination') in excepts:
                            filter_permit = False
                    elif flight_s.validated_data.get('destination').strip() == alert.destinationExcept.strip():
                        filter_permit = False

                if filter_permit:
                    print "EMAIL ENVIADO"
                    send_mail(
                        subject='Alerta: Passagem Rio X {0} - {1} - ida e volta por: R${2}'.format(flight_s.validated_data.get('destination'), flight_s.validated_data.get('departDate').strftime("%d/%m/%Y"), str(flight_s.validated_data.get('price'))),
                        message='<strong>Passagem aérea</strong>\n<strong>Origem:</strong> {0}\n<strong>Destino:</strong> {1}\nData de partida: {2} - Data de retorno: {3}\nPreço: R${4}\n<a href="{5}">Ver no Submarino Viagens</a>'.format(
                            flight_s.validated_data.get('origin'),
                            flight_s.validated_data.get('destination'),
                            flight_s.validated_data.get('departDate').strftime("%d/%m/%Y"),
                            flight_s.validated_data.get('returnDate').strftime("%d/%m/%Y"),
                            str(flight_s.validated_data.get('price')),
                            flight_s.validated_data.get('searchUrl')
                        ),
                        html_message='<h1>Alerta de Passagem Aérea</h1><br /><strong>Origem:</strong> {0}<br /><strong>Destino:</strong> {1}<br />Data de partida: {2} - Data de retorno: {3}<br /><h2>Preço: R${4}</h2><br /><a href="{5}">Ver no Submarino Viagens</a>'.format(
                            flight_s.validated_data.get('origin'),
                            flight_s.validated_data.get('destination'),
                            flight_s.validated_data.get('departDate').strftime("%d/%m/%Y"),
                            flight_s.validated_data.get('returnDate').strftime("%d/%m/%Y"),
                            str(flight_s.validated_data.get('price')),
                            flight_s.validated_data.get('searchUrl')
                        ),
                        from_email='sistema@passagens.com.br', recipient_list=[alert.email])
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
