import json
import ConexionAPI
import ViewMethods

def todasAlertas():
    alertas = ConexionAPI.obtenerObjetoJSON("https://ws.smn.gob.ar/alerts/type/AL")
    alertasStr = ""
    contador = 1
    for p in alertas:
        alertasStr+=f"Alerta n°{contador}\nTitulo: {p['title']}\nEstado: {p['status']}\Fecha: {p['date']}\nHora: {p['hour']}\nDescripcion: {p['description']}\n"
        for i in (p["zones"]).values():
            alertasStr += f"{i}"
            print(i)
        alertasStr+="\n\n"
        print("- - - - - - - - - - - - -")
        contador += 1
    ViewMethods.MostrarAlertasEnVentana(alertasStr)
        
