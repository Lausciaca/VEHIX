from django.urls import path
from .views import *
ordenpatterns = ([
    path('/', ordenes, name='list'),
    path('/create', crear_orden, name='create'),
    path('/orden/<slug:codigo>', ver_orden, name='detail'),
    path('/orden/<slug:codigo>/eliminar', eliminar_orden, name='delete'),
    path('/orden/cambiar_estado/<slug:codigo>/<str:estado>/', cambiar_estado, name='cambiar_estado'),
], 'orden')