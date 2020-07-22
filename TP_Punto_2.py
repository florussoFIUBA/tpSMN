import json
import ConexionAPI

print("Geolocalizacion manual")
usuario_lat = input("Ingrese la latitud: ")
usuario_lon = input("Ingrese la longitud: ")
usuario_ciudad = ""
usuario_prov = ""

pronostico = ConexionAPI.obtenerObjetoJSON("https://ws.smn.gob.ar/map_items/forecast/1") # Uso esto para relacionar la latitud y la longitud con la ciudad / provincia.
alertas = ConexionAPI.obtenerObjetoJSON("https://ws.smn.gob.ar/alerts/type/AL")

for p in pronostico:
    if(usuario_lat == p["lat"]):
        if(usuario_lon == p["lon"]):
            usuario_ciudad = p["name"]
            usuario_prov = p["province"]
print(f"Su ciudad es {usuario_ciudad}, provincia de {usuario_prov}.")

contador = 1
for q in alertas:
    for i in (q["zones"]).values():
        encontrado = usuario_prov in i
        if(encontrado is True):
            print(f"Alerta n°{contador}:")
            print(f"Titulo: {q['title']}")
            print(f"Estado: {q['status']}")
            print(f"Fecha: {q['date']}")
            print(f"Hora: {q['hour']}")
            print(f"Descripcion: {q['description']}")
            print(f"Zona: {i}")
            print("- - - - - - - - - - - - -")
            contador += 1
print("Las alertas involucran su provincia, pero pueden no involucrar su ciudad.")
if(contador == 1):
    print("No se han encontrado alertas para su ciudad.")
