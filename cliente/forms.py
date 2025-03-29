from .models import Cliente
from django import forms

from django import forms
from .models import Cliente

class ClienteForm(forms.ModelForm):
     # Hacer que el email sea opcional
    class Meta:
        model = Cliente
        fields = ['nombre', 'telefono', 'email']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),  # Sin required aquí
        }

   

class ClienteSearchForm(forms.Form):
    search = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
