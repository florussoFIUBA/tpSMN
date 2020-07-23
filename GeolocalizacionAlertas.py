import json
import ConexionAPI
import MetodosLocalizacion
import ViewMethods

def obtenerCiudad():
    usuario_ciudad = ""
    usuario_lista = []
    usuario_ciudad = MetodosLocalizacion.RetornarLocalizacion()
    for i in usuario_ciudad:
        usuario_lista.append(i)
    usuario_lista.remove(" ")
    usuario_ciudad = "".join(usuario_lista)
    return usuario_ciudad

def obtenerURL():
    lista_url = []
    pronostico = ConexionAPI.obtenerObjetoJSON("https://ws.smn.gob.ar/map_items/forecast/1")
    alertas = ConexionAPI.obtenerObjetoJSON("https://ws.smn.gob.ar/alerts/type/AL")
    lista_url = [pronostico,alertas]
    return lista_url
    

def mostrarAlertas():
    usuario_ciudad = obtenerCiudad()
    usuario_prov = ""
    lista_url = obtenerURL()
    chequeo = 0
    alertas = ""
    for p in lista_url[0]:
        if(p["name"] == usuario_ciudad):
            usuario_prov = p["province"]
            chequeo += 1
    if(chequeo == 0):
        print("Su ciudad no se encuentra en la base de datos.")
        
    if(chequeo == 1):
        contador = 1
        for q in lista_url[1]:
            for i in (q["zones"]).values():
                encontrado = usuario_prov in i
                if(encontrado is True):
                    alertas += f"Alerta n°{contador}\nTitulo: {q['title']}\nEstado: {q['status']}\nFecha: {q['date']}\nHora: {q['hour']}\nDescripcion: {q['description']}\nZona: {i}\n"
                    contador += 1
        alertas += "Las alertas involucran su provincia, pero pueden no involucrar su ciudad.\n"
        if(contador == 1):
            alertas += "No se han encontrado alertas para su ciudad.\n\n"
    ViewMethods.MostrarAlertasEnVentana(alertas)
    