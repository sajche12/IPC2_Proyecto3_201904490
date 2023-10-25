from flask import Flask, request, jsonify
from flask_cors import CORS
import xml.etree.ElementTree as ET
from mensaje import Mensaje

app = Flask(__name__)
CORS(app)

# Variables para usar como globales
mensajes = []
palabras_positivas = []
palabras_negativas = []

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
    
    for i in mensajes:
        pass
    
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
    
    for i in palabras_positivas:
        print(f"Positiva: {i}")
    print()
    for j in palabras_negativas:
        print(f"Negativa: {j}")
    
    
    return jsonify({'resultado': 'ok'})

@app.route('/limpiarDatos', methods=['POST'])
def limpiarDatos():
    pass

@app.route('/devolverHashtags', methods=['GET'])
def devolverHashtags():
    pass

@app.route('/devolverMenciones', methods=['GET'])
def devolverMenciones():
    pass

if __name__ == '__main__':
    app.run(debug=True)
