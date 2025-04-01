from django.urls import path
from .views import *
ordenpatterns = ([
    path('/', ordenes, name='list'),
    path('/create', crear_orden, name='create'),
    path('/orden/<slug:codigo>', ver_orden, name='detail'),
    path('/orden/<slug:codigo>/eliminar', eliminar_orden, name='delete'),
    
    
    path('/orden/<slug:codigo>/crear-servicio/', crear_servicio, name='crear_servicio'),
    path('/orden/<slug:codigo>/eliminar-servicio/<int:servicio_id>/', eliminar_servicio, name='eliminar_servicio'),
    
    path('/orden/<slug:codigo>/crear-pago/', crear_pago, name='crear_pago'),
    path('/orden/<slug:codigo>/eliminar-pago/<int:pago_id>/', eliminar_pago, name='eliminar_pago'),
    
    path('/orden/<slug:codigo>/crear-presupuesto/', crear_presupuesto, name='crear_presupuesto'),
    path('/orden/<slug:codigo>/eliminar-presupuesto/', eliminar_presupuesto, name='eliminar_presupuesto'),
    
    
    path('/orden/cambiar_estado/<slug:codigo>/<str:estado>/', cambiar_estado, name='cambiar_estado'),
], 'orden')