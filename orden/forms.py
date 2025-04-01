from django import forms
from .models import *

class OrdenSearchForm(forms.Form):
    search = forms.CharField(required=False)



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
        
        

class CrearPresupuestoForm(forms.ModelForm):
    class Meta:
        model = Presupuesto
        fields = ['monto']
        widgets = {
            'monto': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0'
            }),
        }
        labels = {
            'monto': 'Monto del Presupuesto ($)',
        }
        

class CrearServicioForm(forms.ModelForm):
    class Meta:
        model = Servicio
        fields = ['servicio']
        widgets = {
            'servicio': forms.TextInput(attrs={'placeholder': 'Servicio a realizar'})  # Si necesitas algún tipo de widget específico
        }
        labels = {
            'servicio': 'Servicio a realizar',
        }


class CrearPagoForm(forms.ModelForm):
    class Meta:
        model = Pago
        fields = ['monto']
        widgets = {
            'monto': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0'
            }),
        }
        labels = {
            'monto': 'Monto del pago ($)',
        }