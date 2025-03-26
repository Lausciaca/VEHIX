from django import forms
from .models import Orden, ImagenVehiculo
from cliente.models import Cliente
from vehiculo.models import Vehiculo
from datetime import datetime

class OrdenSearchForm(forms.Form):
    search = forms.CharField(required=False)
    estado = forms.ChoiceField(choices=Orden.ESTADOS_CHOICES, required=False)
    cobertura = forms.ChoiceField(choices=Orden.COBERTURAS_CHOICES, required=False)


class OrdenForm(forms.ModelForm):
    class Meta:
        model = Orden
        fields = ['cliente', 'vehiculo', 'cobertura', 'estado']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-control'}),
            'vehiculo': forms.Select(attrs={'class': 'form-control'}),
            'cobertura': forms.Select(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
        }

class ImagenVehiculoForm(forms.ModelForm):
    class Meta:
        model = ImagenVehiculo
        fields = ['imagen']  # Los campos de las imágenes
        widgets = {
            'imagen': forms.ClearableFileInput(attrs={'multiple': True})
        }