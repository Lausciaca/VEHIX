from django import forms
from .models import Orden

class OrdenSearchForm(forms.Form):
    cliente = forms.CharField(required=False)
    vehiculo = forms.CharField(required=False)
    estado = forms.ChoiceField(choices=Orden.ESTADOS_CHOICES, required=False)
    cobertura = forms.ChoiceField(choices=Orden.COBERTURAS_CHOICES, required=False)
