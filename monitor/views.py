# -*- coding: utf-8 -*-

from django.core.mail import send_mail
from monitor.models import Flight
from monitor.serializers import FlightSerializer
from rest_framework import generics
import logging

logger = logging.getLogger(__name__)

class ExtentListCreateAPIView(generics.ListCreateAPIView):
    """
    Concrete view for listing a queryset or creating a model instance.
    """

    def post(self, request, *args, **kwargs):
    	flight_s = FlightSerializer(data=request.data)
    	if (flight_s.is_valid()):
    		flight = flight_s.save()
    		if (flight.price < 500):
    			print "ENVIA E-MAIL DE ALERTA"
    			send_mail("Alerta de preço de passagem: ".decode('utf8')+flight.destination, flight.searchUrl, 'sistema@passagens.com.br',['jonatascastro12@gmail.com'])    		

        return self.create(request, *args, **kwargs)


# Create your views here.
class FlightList(ExtentListCreateAPIView):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer


class FlightDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer