import json
import requests

#Constantes
PRONOSTICO1D = "https://ws.smn.gob.ar/map_items/forecast/1"
PRONOSTICO2D = "https://ws.smn.gob.ar/map_items/forecast/2"
PRONOSTICO3D = "https://ws.smn.gob.ar/map_items/forecast/3"
ALERTAS = "https://ws.smn.gob.ar/alerts/type/AL"
ESTADO_ACTUAL = "https://ws.smn.gob.ar/map_items/weather"

#Variables
headers = {'Content-Type':'application/json',
            'Authorization':''}
'''
Obtiene informacion de la API correspondiente a url.
Devuelve un JSON string formateado.
'''
def obtenerSMNjson(url):
    
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        rawJson = json.loads(response.content.decode('utf-8'))
        return json.dumps(rawJson, sort_keys=True, indent=4, default=rawJson)
    else:
        return None

'''
Transforma el JSON devuelto por la API en un objeto de Python.
'''
def obtenerObjetoJSON(url):
    info = obtenerSMNjson(url)
    
    if info is not None:
        objJson=json.loads(info)
        print(objJson)
    else:
        objJson= None
    
    return objJson

