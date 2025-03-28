from django import forms
from .models import *

# class OrdenSearchForm(forms.Form):
#     search = forms.CharField(required=False)
#     estado = forms.ChoiceField(choices=Orden.ESTADOS_CHOICES, required=False)
#     cobertura = forms.ChoiceField(choices=Orden.COBERTURAS_CHOICES, required=False)


class OrdenParticularForm(forms.ModelForm):
    class Meta:
        model = OrdenParticular
        fields = ['estado']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-control'}),
            'vehiculo': forms.Select(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
        }
        
class OrdenTercerosForm(forms.ModelForm):
    class Meta:
        model = OrdenTerceros
        fields = ['estado']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-control'}),
            'vehiculo': forms.Select(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
        }
        
class OrdenRiesgoForm(forms.ModelForm):
    class Meta:
        model = OrdenRiesgo
        fields = ['estado']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-control'}),
            'vehiculo': forms.Select(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
        }
        
class OrdenRecuperoForm(forms.ModelForm):
    class Meta:
        model = OrdenRecupero
        fields = ['estado']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-control'}),
            'vehiculo': forms.Select(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
        }

class ImagenVehiculoForm(forms.ModelForm):
    imagen = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}))  # Permite subir varias imágenes

    class Meta:
        model = ImagenVehiculo
        fields = ['imagen']