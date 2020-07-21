import json
import ConexionAPI

un_dia = ConexionAPI.obtenerObjetoJSON("https://ws.smn.gob.ar/map_items/forecast/1")
dos_dias = ConexionAPI.obtenerObjetoJSON("https://ws.smn.gob.ar/map_items/forecast/2")
tres_dias = ConexionAPI.obtenerObjetoJSON("https://ws.smn.gob.ar/map_items/forecast/3")
alertas = ConexionAPI.obtenerObjetoJSON("https://ws.smn.gob.ar/alerts/type/AL")
lista = [un_dia,dos_dias,tres_dias]

def verPronostico(objJson,ciudad,provincia):
    for p in objJson:
        if(p["name"] == ciudad):
            provincia = p["province"]
            print(f"Pronostico dentro de {lista.index(objJson)+1} dia(s):")
            print(f"Por la mañana, el clima es: {p['weather']['morning_desc']}. La temperatura es de {p['weather']['morning_temp']}°C.")
            print(f"Por la tarde, el clima es: {p['weather']['afternoon_desc']}. La temperatura es de {p['weather']['afternoon_temp']}°C.")
    mostrarAlertas(provincia)
        
def mostrarAlertas(provincia):
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
    
def menu():
    print("Bienvenido al menú de pronósticos del Servicio Meteorologico Nacional")
    opcion = int(input("Ver pronostico y alertas para: \n1) Un día\n2) Dos días\n3) Tres días\n4) Salir\n"))
    while(opcion != 1 and opcion != 2 and opcion != 3 and opcion != 4):
        print("Opcion inválida")
        opcion = int(input("1) Un día\n2) Dos días\n3) Tres días\n4) Salir\n"))
    fin = "y"
    provincia = ""
    while(fin != "n"):
        if(opcion == 1):
            ciudad = input("Ingrese su ciudad: ")
            verPronostico(un_dia,ciudad,provincia)
            fin = "n"
        if(opcion == 2):
            ciudad = input("Ingrese su ciudad: ")
            verPronostico(dos_dias,ciudad,provincia)
            fin = "n"
        if(opcion == 3):
            ciudad = input("Ingrese su ciudad: ")
            verPronostico(tres_dias,ciudad,provincia)
            fin = "n"
        if(opcion == 4):
            fin = "n"
def main():
    menu()
main()

