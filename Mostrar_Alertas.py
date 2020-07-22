import json
import ConexionAPI

alertas = ConexionAPI.obtenerObjetoJSON("https://ws.smn.gob.ar/alerts/type/AL")

contador = 1
for p in alertas:
    print(f"Alerta n°{contador}:")
    print(f"Titulo: {p['title']}")
    print(f"Estado: {p['status']}")
    print(f"Fecha: {p['date']}")
    print(f"Hora: {p['hour']}")
    print(f"Descripcion: {p['description']}")
    print(f"Zonas:")
    for i in (p["zones"]).values():
        print(i)
    print("- - - - - - - - - - - - -")
    contador += 1
        
