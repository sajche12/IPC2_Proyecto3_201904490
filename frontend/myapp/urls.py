from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio),
    path('limpiarDatos/', views.resetear_datos),
    path('grabarMensajes/', views.grabarMensajes),
    path('grabarConfiguracion/', views.grabarConfiguracion),
    path('peticiones/', views.peticiones),
    path('peticiones/devolverHashtags/', views.devolverHashtags, name='devolverHashtags'),
    path('peticiones/devolverMenciones/', views.devolverMenciones),
    path('peticiones/devolverSentimientos/', views.devolverSentimientos)
]