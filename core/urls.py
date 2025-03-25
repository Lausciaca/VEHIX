from django.urls import path, include
from . import views
from orden.views import ordenes, crear_orden

urlpatterns = [
    path('', views.index, name='index'),
    path('ordenes', ordenes, name='ordenes'),
    path('ordenes/create', crear_orden, name='ordenes-create'),
]