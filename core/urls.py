from django.urls import path, include
from . import views
from orden.urls import ordenpatterns
from cliente.urls import clientepatterns

urlpatterns = [
    path('', views.index, name='index'),
    path('clientes', include(clientepatterns)),
    path('ordenes', include(ordenpatterns)),
]