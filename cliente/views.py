from django.shortcuts import render
from .models import Cliente
from django.views.generic.edit import CreateView
from .forms import ClienteSearchForm

# Create your views here.
def clientes(request):
    form = ClienteSearchForm(request.GET)
    clientes = Cliente.objects.all()
    
    if form.is_valid():
        if form.cleaned_data['search']:
            clientes = clientes.filter(nombre__icontains=form.cleaned_data['search'])


    
    return render(request, 'cliente/clientes.html', {
        'clientes': clientes,
        'form': form,
        })
    
    
class ClienteCreateView(CreateView):
    model = Cliente