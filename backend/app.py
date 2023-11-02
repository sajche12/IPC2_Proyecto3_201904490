from flask import Flask, request, jsonify
from flask_cors import CORS
import xml.etree.ElementTree as ET
from mensaje import Mensaje
import re

app = Flask(__name__)
CORS(app)


# Variables para usar como globales
mensajes = []
palabras_positivas = []
palabras_negativas = []
fechas = []
horas = []
hashtags = []
menciones = []


@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/grabarMensajes', methods=['POST'])
def grabarMensajes():
    global mensajes
    # en este metodo se recibira un xml con los mensajes y se grabaran en la base de datos
    xml_file = request.files['entrada_mensajes']
    
    # Parse the XML file
    xml_data = xml_file.read()
    root = ET.fromstring(xml_data)
    
    # leer los mensajes del xml y guardarlos en la lista mensajes
    for mensaje in root.findall('MENSAJE'):
        fecha = mensaje.find('FECHA').text
        texto = mensaje.find('TEXTO').text
        mensaje_nuevo = Mensaje(fecha, texto)
        mensajes.append(mensaje_nuevo)
    
    # retornar un messagebox con el mensaje de que se grabaron los mensajes
    return jsonify({'resultado': 'ok'})

@app.route('/grabarConfiguracion', methods=['POST'])
def grabarConfiguracion():
    global palabras_positivas, palabras_negativas
    # en este metodo se recibira un xml con los mensajes y se grabaran en la base de datos
    xml_file = request.files['entrada_configuraciones']
    
    # Parse the XML file
    xml_data = xml_file.read()
    root = ET.fromstring(xml_data)
    
    # Iterar sobre los elementos y agregar palabras a las listas correspondientes
    for elemento_sentimiento in root:
        for palabra in elemento_sentimiento:
            if elemento_sentimiento.tag == 'sentimientos_positivos':
                palabras_positivas.append(palabra.text.strip())
            elif elemento_sentimiento.tag == 'sentimientos_negativos':
                palabras_negativas.append(palabra.text.strip())
    
    return jsonify({'resultado': 'ok'})

@app.route('/limpiarDatos', methods=['POST'])
def limpiarDatos():
    global mensajes, palabras_positivas, palabras_negativas, fechas, horas, hashtags, menciones
    mensajes = []
    palabras_positivas = []
    palabras_negativas = []
    fechas = []
    horas = []
    hashtags = []
    menciones = []
    
    return jsonify({'resultado': 'ok'})

@app.route('/devolverHashtags', methods=['GET'])
def devolverHashtags():
    global mensajes, fechas, horas, hashtags
    datos_hashtags = []
    
    # Definir la expresión regular
    patron_fecha = re.compile(r"\b(\d{2}/\d{2}/\d{4})") # Captura la fecha en el formato dd/mm/yyyy.
    patron_hora = re.compile(r"\b(\d{1,2}):(\d{2}) hrs\.\b")    # Captura la hora en el formato hh:mm hrs.
    patron_hashtags = r"#(.*?)#"   # Captura los hashtags.
    
    for i in mensajes:
        
        # Buscar fecha y hora en los patrones
        buscar_fecha = patron_fecha.search(i.fecha)
        buscar_hora = patron_hora.search(i.fecha)
        
        if buscar_fecha != None:
            fecha = buscar_fecha.group(1)
            fechas.append(fecha)
        else:
            fecha = ''
            fechas.append(fecha)
        
        # Buscar los patrones en el texto
        resultados = re.findall(patron_hashtags, i.texto)
        
        # agregar los hashtags a la lista
        for hashtag in resultados:
            dato_nuevo = {}
            hashtags.append(f"#{hashtag}#")
            if str('#'+hashtag+'#') in hashtags:
                dato_nuevo['fecha'] = fecha
                dato_nuevo['hashtag'] = f"#{hashtag}#"
                datos_hashtags.append(dato_nuevo)
            elif str('#'+hashtag+'#') not in hashtags:
                dato_nuevo['fecha'] = fecha
                dato_nuevo['hashtag'] = f"#{hashtag}#"
                datos_hashtags.append(dato_nuevo)
        
    for i in datos_hashtags:
        # Buscar la cantidad de veces que se repite el hashtag
        contador = 0
        for j in datos_hashtags:
            if i['hashtag'] == j['hashtag']:
                contador += 1
        i['cantidad'] = contador
        contador = 0
               
    # retornar datos_hashtags
    return datos_hashtags

# Método para devolver los datos con la cantidad de cada

@app.route('/devolverMenciones', methods=['GET'])
def devolverMenciones():
    global mensajes, fechas, menciones
    datos_menciones = []
    
    # Definir la expresión regular para extraer el texto después de @
    patron_fecha = re.compile(r"\b(\d{2}/\d{2}/\d{4})") # Captura la fecha en el formato dd/mm/yyyy.
    patron_menciones = r"@(\w+)"
    
    for i in mensajes:
        
        # Buscar fecha y hora en los patrones
        buscar_fecha = patron_fecha.search(i.fecha)
        
        if buscar_fecha != None:
            fecha = buscar_fecha.group(1)
        else:
            fecha = ''
            
        # Buscar los patrones en el texto
        resultados = re.findall(patron_menciones, i.texto)
        
        # agregar las menciones a la lista
        for mencion in resultados:
            dato_nuevo = {}
            menciones.append(f"@{mencion}")
            if str('@'+mencion) in menciones:
                dato_nuevo['fecha'] = fecha
                dato_nuevo['mencion'] = f"@{mencion}"
                datos_menciones.append(dato_nuevo)
            elif str('@'+mencion) not in menciones:
                dato_nuevo['fecha'] = fecha
                dato_nuevo['mencion'] = f"@{mencion}"
                datos_menciones.append(dato_nuevo)
                
    for i in datos_menciones:
        # Buscar la cantidad de veces que se repite la mención
        contador = 0
        for j in datos_menciones:
            if i['mencion'] == j['mencion']:
                contador += 1
        i['cantidad'] = contador
        contador = 0
    
    return datos_menciones

@app.route('/devolverSentimientos', methods=['GET'])
def devolverSentimientos():
    global mensajes, palabras_positivas, palabras_negativas, fechas
    datos_sentimientos = []
    
    # Definir la expresión regular para extraer el texto después de @
    patron_fecha = re.compile(r"\b(\d{2}/\d{2}/\d{4})") # Captura la fecha en el formato dd/mm/yyyy.
    
    for i in mensajes:
            
            # Buscar fecha y hora en los patrones
            buscar_fecha = patron_fecha.search(i.fecha)
            
            if buscar_fecha != None:
                fecha = buscar_fecha.group(1)
            else:
                fecha = ''
                
            # Buscar los patrones en el texto
            for palabra in palabras_positivas:
                if palabra in i.texto:
                    dato_nuevo = {}
                    dato_nuevo['fecha'] = fecha
                    dato_nuevo['sentimiento'] = palabra
                    dato_nuevo['valor'] = 'positivo'
                    datos_sentimientos.append(dato_nuevo)
                    
            for palabra in palabras_negativas:
                if palabra in i.texto:
                    dato_nuevo = {}
                    dato_nuevo['fecha'] = fecha
                    dato_nuevo['sentimiento'] = palabra
                    dato_nuevo['valor'] = 'negativo'
                    datos_sentimientos.append(dato_nuevo)
                    
    for i in datos_sentimientos:
        # Buscar la cantidad de veces que se repite el sentimiento
        contador = 0
        for j in datos_sentimientos:
            if i['sentimiento'] == j['sentimiento']:
                contador += 1
        i['cantidad'] = contador
        contador = 0
        
    return datos_sentimientos
     

if __name__ == '__main__':
    app.run(debug=True)
