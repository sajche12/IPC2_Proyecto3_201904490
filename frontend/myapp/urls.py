from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio),
    path('limpiarDatos/', views.resetear_datos),
    path('grabarMensajes/', views.grabarMensajes),
    path('grabarConfiguracion/', views.grabarConfiguracion),
    path('peticiones/', views.peticiones),
    path('peticiones/devolverHashtags/', views.devolverHashtags, name='devolverHashtags'),
    path('peticiones/devolverMenciones/', views.devolverMenciones, name='devolverMenciones'),
    path('peticiones/devolverSentimientos/', views.devolverSentimientos, name='devolverSentimientos'),
    path('peticiones/graficas/', views.graficas, name='graficas'),
    path('peticiones/ayuda/', views.ayuda, name='ayuda'),
    path('peticiones/ayuda/informacion/', views.informacion, name='informacion'),
]