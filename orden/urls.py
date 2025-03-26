from django.urls import path
from .views import ordenes, crear_orden, ver_orden, eliminar_orden

ordenpatterns = ([
    path('', ordenes, name='list'),
    path('/create', crear_orden, name='create'),
    path('/orden/<slug:codigo>', ver_orden, name='detail'),
    path('/orden/<slug:codigo>/eliminar', eliminar_orden, name='delete'),
], 'orden')