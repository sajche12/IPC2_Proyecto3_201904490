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
        return render(request, 'consultarHashtags.html', {'fechas': fechas, 'hashtags': hashtags, 'fecha_analizar': fecha_analizar, 'contador': contador})
    
    return render(request, 'consultarHashtags.html', {'fechas': fechas})

def devolverMenciones(request):
    fechas = []
    # llamar al endpoint de menciones del backend
    response = requests.get('http://localhost:5000/devolverMenciones')
    data = response.json()
    for i in data:
        if i['fecha'] not in fechas:
            fechas.append(i['fecha'])
    fecha_analizar = request.GET.get('fecha')
    if fecha_analizar:
        menciones = []
        contador = []
        for i in data:
            if i['fecha'] == fecha_analizar:
                if i['mencion'] not in menciones:
                    menciones.append(i['mencion'])
                    contador.append(i['cantidad'])
        return render(request, 'consultarMenciones.html', {'fechas': fechas, 'menciones': menciones, 'fecha_analizar': fecha_analizar, 'contador': contador})
    
    return render(request, 'consultarMenciones.html', {'fechas': fechas})

def devolverSentimientos(request):
    fechas = []
    # llamar al endpoint de sentimientos del backend
    response = requests.get('http://localhost:5000/devolverSentimientos')
    data = response.json()
    cambio_fecha = False
    for i in data:
        if i['fecha'] not in fechas:
            fechas.append(i['fecha'])
    fecha_analizar = request.GET.get('fecha')
    if fecha_analizar:
        positivos = 0
        negativos = 0
        neutro = 0
        for i in data:
            if i['fecha'] == fecha_analizar:
                cambio_fecha = True
                if i['valor'] == 'positivo':
                    positivos += 1
                elif i['valor'] == 'negativo':
                    negativos += 1
        return render(request, 'consultarSentimientos.html', {'fechas': fechas, 'positivos': positivos, 'fecha_analizar': fecha_analizar, 'negativos': negativos, 'neutro': neutro, 'cambio_fecha': True})
    
    return render(request, 'consultarSentimientos.html', {'fechas': fechas, 'cambio_fecha': cambio_fecha})

def graficas(request):
    return render(request, 'graficas.html')

def ayuda(request):
    return render(request, 'ayuda.html')

def informacion(request):
    return render(request, 'informacion.html')
    
    