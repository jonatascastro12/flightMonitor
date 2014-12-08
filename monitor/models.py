# -*- coding: utf-8 -*-
from django.db import models
from django.contrib import admin
from django import forms
from django.utils.html import conditional_escape, format_html
from django.forms.utils import flatatt, to_current_timezone
from django.utils.safestring import mark_safe



class BitChoices(object):
	def __init__(self, choices):
		self._choices = []
		self._lookup = {}
		for index, (key, val) in enumerate(choices):
			index = 2**index
			self._choices.append((index, val))
			self._lookup[key] = index

	def __iter__(self):
		return iter(self._choices)

	def __len__(self):
		return len(self._choices)

	def __getattr__(self, attr):
		try:
			return self._lookup[attr]
		except KeyError:
			raise AttributeError(attr)

	def get_selected_keys(self, selection):
		""" Return a list of keys for the given selection """
		return [ k for k,b in self._lookup.iteritems() if b & selection]

	def get_selected_values(self, selection):
		""" Return a list of values for the given selection """
		return [ b for b,v in self._choices if b & selection]

WEEKDAY = BitChoices((('seg', 'Segunda'), ('ter', 'Terça'), ('qua', 'Quarta'),
	('qui', 'Quinta'), ('sex', 'Sexta'), ('sab', 'Sábado'),
        ('dom', 'Domingo')
           ))      

# Create your models here.
class Flight(models.Model):
	departDate = models.DateField()
	returnDate = models.DateField()
	origin = models.CharField(max_length=250)
	destination = models.CharField(max_length=250, db_index=True)
	searchUrl = models.CharField(max_length=600)
	price = models.DecimalField(max_digits=6, decimal_places=2, db_index=True)
	timestamp =  models.DateTimeField(auto_now_add=True, blank=True)

class FilterAlert(models.Model):
	destinationFilter = models.CharField(max_length=250, blank=True, null=True)
	email = models.EmailField()
	maxPrice = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
	dateStart = models.DateField(blank=True, null=True)
	dateEnd = models.DateField(blank=True, null=True)
	active = models.BooleanField(default=False)
	weekday = models.PositiveIntegerField(default=0)

class FlightAdmin(admin.ModelAdmin):
	list_display = ('departDate','returnDate','destination','price','timestamp')
	list_filter = ['destination', 'departDate','timestamp']

class BinaryWidget(forms.CheckboxSelectMultiple):
	def render(self, name, value, attrs=None, choices=()):
		if value is None:
	        	value = 0
		choices = self.choices
		final_attrs = self.build_attrs(attrs, name=name)
		output = [format_html('<select multiple="multiple"{0}>', flatatt(final_attrs))]
	
		value = WEEKDAY.get_selected_values(value)

		options = self.render_options(choices, value)
		if options:
	        	output.append(options)
		output.append('</select>')
	        return mark_safe('\n'.join(output))

	def value_from_datadict(self, data, files, name):
        	value = super(BinaryWidget, self).value_from_datadict(data, files, name)
	        if name == 'weekday':
			value = sum(int(i) for i in value)
		return value


class FilterAlertForm(forms.ModelForm):
	weekday = forms.IntegerField(widget=BinaryWidget(choices=WEEKDAY))
	class Meta:
		model = FilterAlert

class FilterAlertAdmin(admin.ModelAdmin):
	form = FilterAlertForm
	list_display = ('email', 'maxPrice', 'destinationFilter', 'active')
	
