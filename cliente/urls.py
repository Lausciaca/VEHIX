from django.urls import path
from .views import clientes, ClienteCreateView

clientepatterns = ([
    path('', clientes, name='list'),
    path('create', ClienteCreateView.as_view(), name='create'),
], 'cliente')