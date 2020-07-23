import json
import ConexionAPI
import LocationMethods

usuario_prov = ""
usuario_lista = []

usuario_ciudad = LocationMethods.ReturnAddress()
for i in usuario_ciudad:
    usuario_lista.append(i)
usuario_lista.remove(" ")
usuario_ciudad = "".join(usuario_lista)
print(f"Su ciudad es: {usuario_ciudad}")

pronostico = ConexionAPI.obtenerObjetoJSON("https://ws.smn.gob.ar/map_items/forecast/1")
alertas = ConexionAPI.obtenerObjetoJSON("https://ws.smn.gob.ar/alerts/type/AL")

chequeo = 0
for p in pronostico:
    if(p["name"] == usuario_ciudad):
        usuario_prov = p["province"]
        chequeo += 1
if(chequeo == 0):
    print("Su ciudad no se encuentra en la base de datos.")
        
if(chequeo == 1):
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