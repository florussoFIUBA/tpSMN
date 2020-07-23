import json
import ConexionAPI

def obtenerURL():
    lista_url = []
    un_dia = ConexionAPI.obtenerObjetoJSON("https://ws.smn.gob.ar/map_items/forecast/1")
    dos_dias = ConexionAPI.obtenerObjetoJSON("https://ws.smn.gob.ar/map_items/forecast/2")
    tres_dias = ConexionAPI.obtenerObjetoJSON("https://ws.smn.gob.ar/map_items/forecast/3")
    alertas = ConexionAPI.obtenerObjetoJSON("https://ws.smn.gob.ar/alerts/type/AL")
    lista_url = [un_dia,dos_dias,tres_dias]
    return lista_url

def mostrarData(lista_url):
    print("- - - - - - TORMENTA - - - - - -")

    provincia = ""
    chequeo = 0

    while(chequeo == 0):
        ciudad = input("Ingrese su ciudad: ")
        for url in lista_url:
            for p in url:
                if(p["name"] == ciudad):
                    chequeo += 1
                    provincia = p["province"]
                    print(f"Día {lista.index(url)+1}")
                    print(f"Temperatura a la mañana: {p['weather']['morning_temp']}°C - Clima a la mañana: {p['weather']['morning_desc']}")
                    print(f"Temperatura a la tarde: {p['weather']['afternoon_temp']}°C - Clima a la tarde: {p['weather']['afternoon_desc']}")
                    print("- - - - - - - - - - - - - - - -")
        if(chequeo == 0):
            print("La ciudad ingresada no se encuentra en la base de datos. Intente nuevamente.")

    contador = 1
    for q in alertas:
        for i in (q["zones"]).values():
            encontrado = provincia in i
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
        print("No se han encontrado alertas para su provincia.")
