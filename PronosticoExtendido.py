import json
import ConexionAPI
import ViewMethods

def obtenerURL():
    lista_url = []
    un_dia = ConexionAPI.obtenerObjetoJSON("https://ws.smn.gob.ar/map_items/forecast/1")
    dos_dias = ConexionAPI.obtenerObjetoJSON("https://ws.smn.gob.ar/map_items/forecast/2")
    tres_dias = ConexionAPI.obtenerObjetoJSON("https://ws.smn.gob.ar/map_items/forecast/3")
    lista_url = [un_dia,dos_dias,tres_dias]
    return lista_url

def ObtenerAlertas():
    return ConexionAPI.obtenerObjetoJSON("https://ws.smn.gob.ar/alerts/type/AL")

def mostrarData(ciudad):
    lista_url = obtenerURL()
    provincia = ""
    chequeo = 0
    alertasStr = ""
    alertas = ObtenerAlertas()
    while(chequeo == 0):
        for url in lista_url:
            for p in url:
                if(p["name"] == ciudad):
                    chequeo += 1
                    provincia = p["province"]
                    alertasStr+=f"Día {lista_url.index(url)+1}\nTemperatura a la mañana: {p['weather']['morning_temp']}°C - Clima a la mañana: {p['weather']['morning_desc']}\nTemperatura a la tarde: {p['weather']['afternoon_temp']}°C - Clima a la tarde: {p['weather']['afternoon_desc']}"
        if(chequeo == 0):
            alertasStr+="La ciudad ingresada no se encuentra en la base de datos. Intente nuevamente."

    contador = 1
    for q in alertas:
        for i in (q["zones"]).values():
            encontrado = provincia in i
            if(encontrado is True):
                alertasStr+=f"Alerta n°{contador}:\nTitulo: {q['title']}\nEstado: {q['status']}\nFecha: {q['date']}\nHora: {q['hour']}\nDescripcion: {q['description']}\Zona: {i}\nLas alertas involucran su provincia, pero pueden no involucrar su ciudad."
                contador += 1
    if(contador == 1):
        alertasStr+="No se han encontrado alertas para su provincia.\n"
    ViewMethods.MostrarAlertasEnVentana(alertas)
