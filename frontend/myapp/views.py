from django.shortcuts import render
import requests

# Create your views here.
def inicio(request):
    return render(request, 'base.html')

def resetear_datos(request):
    return render(request, 'resetearDatos.html')
    
def grabarMensajes(request):
    return render(request, 'cargarMensajes.html')

def grabarConfiguracion(request):
    return render(request, 'cargarConfiguracion.html')

def peticiones(request):
    return render(request, 'peticiones.html')

def devolverHashtags(request):
    fechas = []
    # llamar al endpoint de hashtags del backend
    response = requests.get('http://localhost:5000/devolverHashtags')
    data = response.json()
    for i in data:
        if i['fecha'] not in fechas:
            fechas.append(i['fecha'])
    
    fecha_analizar = request.GET.get('fecha')
    if fecha_analizar:
        hashtags = []
        contador = []
        for i in data:
            if i['fecha'] == fecha_analizar:
                if i['hashtag'] not in hashtags:
                    hashtags.append(i['hashtag'])
                    contador.append(i['cantidad'])
        print(hashtags)
        print(contador)
        return render(request, 'consultarHashtags.html', {'fechas': fechas, 'hashtags': hashtags, 'fecha_analizar': fecha_analizar, 'contador': contador})
    
    
    
    
    return render(request, 'consultarHashtags.html', {'fechas': fechas})

def devolverMenciones(request):
    return render(request, 'consultarMenciones.html')

def devolverSentimientos(request):
    return render(request, 'consultarSentimientos.html')
    
    