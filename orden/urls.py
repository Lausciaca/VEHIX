from django.urls import path
from .views import ordenes, crear_orden

ordenpatterns = ([
    path('', ordenes, name='list'),
    path('create', crear_orden, name='create'),
], 'orden')