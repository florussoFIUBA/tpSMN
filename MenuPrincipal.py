import tkinter as tk
import ViewMethods
import json
import requests
import geocoder
from geopy.geocoders import Nominatim
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
import tkinter.scrolledtext as tkscrolled

PRONOSTICO1D = "https://ws.smn.gob.ar/map_items/forecast/1"
PRONOSTICO2D = "https://ws.smn.gob.ar/map_items/forecast/2"
PRONOSTICO3D = "https://ws.smn.gob.ar/map_items/forecast/3"
ALERTAS_URL = "https://ws.smn.gob.ar/alerts/type/AL"

headers = {'Content-Type':'application/json',
            'Authorization':''}

def obtenerSMNjson(url):
    '''Recibe un link url, y devuelve un archivo Json "crudo".
    '''
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        rawJson = json.loads(response.content.decode('utf-8'))
        return json.dumps(rawJson, sort_keys=True, indent=4, default=rawJson)
    else:
        return None
    
def obtenerObjetoJSON(url):
    '''Recibe un Json "crudo" y lo devuelve como un objeto Json para que pueda ser abierto e interpretado facilmente.
    '''
    info = obtenerSMNjson(url)
    
    if info is not None:
        objJson=json.loads(info)
    else:
        objJson= None
    
    return objJson

def MostrarAlertasEnVentana(texto):
    '''Recibe una cadena
    Abre un cuadro de texto e imprime la cadena dentro de dicho cuadro.
    '''
    if(texto!=""):
        txtBoxWitdth, txtBoxHeight = 200, 200
        ventanaAlertas = tk.Tk()
        ventanaAlertas.geometry("250x250")
        ventanaAlertas.title("Alertas")
        txtBoxScroll = tkscrolled.ScrolledText(master = ventanaAlertas, width = txtBoxWitdth, height = txtBoxHeight, wrap='word')
        txtBoxScroll.insert(index = 1.0, chars = texto)
        txtBoxScroll.pack()
        ventanaAlertas.mainloop()
    else:
        messagebox.showinfo("Alertas", "No se registraron alertas")

def obtenerURL():
    '''Crea una lista con los jsons de los pronosticos para cada dia, para poder iterar cada dia de pronosticos en la funcion verPronostico.
    '''
    lista_url = []
    un_dia = obtenerObjetoJSON(PRONOSTICO1D)
    dos_dias = obtenerObjetoJSON(PRONOSTICO2D)
    tres_dias = obtenerObjetoJSON(PRONOSTICO3D)
    lista_url = [un_dia,dos_dias,tres_dias]
    return lista_url

def todasAlertas(provincia,alertasStr):
    '''Recibe una provincia
    Devuelve en pantalla las alertas que involucran la provincia.
    Si se recibe '0' como provincia, muestra todas las alertas sin filtrar.
    '''
    ALERTAS_URL = "https://ws.smn.gob.ar/alerts/type/AL"
    alertas = obtenerObjetoJSON(ALERTAS_URL)
    contador = 1
    if(provincia == '0'):
        for p in alertas:
            alertasStr+=f"Alerta n°{contador}\nTitulo: {p['title']}\nEstado: {p['status']}\Fecha: {p['date']}\nHora: {p['hour']}\nDescripcion: {p['description']}\nZonas: \n"
            for i in (p["zones"]).values():
                alertasStr += f"{i}\n"
            alertasStr+="\n\n"
            contador += 1
        MostrarAlertasEnVentana(alertasStr)
    else:
        for q in alertas:
            for i in (q["zones"]).values():
                encontrado = provincia in i
                if(encontrado is True):
                    alertasStr+=f"Alerta n°{contador}:\nTitulo: {q['title']}\nEstado: {q['status']}\nFecha: {q['date']}\nHora: {q['hour']}\nDescripcion: {q['description']}\Zona: {i}\nLas alertas involucran su provincia, pero pueden no involucrar su ciudad."
                    contador += 1
        if(contador == 1):
            alertasStr+="No se han encontrado alertas para su provincia.\n"
        MostrarAlertasEnVentana(alertasStr)

def verPronostico(ciudad):
    '''Recibe una ciudad ingresada por el usuario.
    En caso de encontrar la ciudad en la base de datos, devuelve en pantalla el pronostico extendido para esa ciudad, y llama a la funcion de verAlertas con la provincia donde se encuentra la ciudad.
    '''
    lista_url = obtenerURL()
    provincia = ""
    chequeo = 0
    alertasStr = ""
    for url in lista_url:
        for p in url:
            if(p["name"] == ciudad):
                chequeo += 1
                provincia = p["province"]
                alertasStr+=f"Día {lista_url.index(url)+1}\nTemperatura a la mañana: {p['weather']['morning_temp']}°C - Clima a la mañana: {p['weather']['morning_desc']}\nTemperatura a la tarde: {p['weather']['afternoon_temp']}°C - Clima a la tarde: {p['weather']['afternoon_desc']}\n"
    if(chequeo == 0):
        alertasStr+="La ciudad ingresada no se encuentra en la base de datos. Intente nuevamente."
        MostrarAlertasEnVentana(alertasStr)
    todasAlertas(provincia,alertasStr)
        
def RetornarLocalizacionActual():
    '''Usando la libreria geocoder, devuelve una geolocalizacion (lat long).
    '''
    myLocation = geocoder.ip('me')
    return myLocation.latlng

def RetornarLocalizacion(localidad):
    '''Recibe una localidad, puede ser 'ciudad' o 'provincia'.
    Devuelve la 'ciudad' o 'provincia' donde se encuentra el usuario, respectivamente.
    '''
    try:
        latLong = RetornarLocalizacionActual()
        geolocator = Nominatim(user_agent="tp2")
        location = geolocator.reverse(f"{latLong[0]}, {latLong[1]}")
        if(localidad == 'provincia'):
            provincia = location.address.split(',')[len(location.address.split(','))-3]
            usuario_lista = []
            for i in provincia:
                usuario_lista.append(i)
            usuario_lista.remove(" ")
            provincia = "".join(usuario_lista)
            return provincia
        elif(localidad == 'ciudad'):
            ciudad = location.address.split(',')[len(location.address.split(','))-7]
            usuario_lista = []
            for i in ciudad:
                usuario_lista.append(i)
            usuario_lista.remove(" ")
            ciudad = "".join(usuario_lista)
            return ciudad
    except:
        errorStr = "No ha sido posible la conexion con el servidor de geolocalizacion."
        MostrarAlertasEnVentana(errorStr)
    
def CrearVentanaPrincipal():
    ventanaPrincipal = tk.Tk()
    ventanaPrincipal.geometry("300x340")
    ventanaPrincipal.title("Tormenta")
    tk.Label(ventanaPrincipal, text="Bienvenidos a Tormenta").pack()
    btn_OptionOne = tk.Button(ventanaPrincipal, text = "Listar alertas por localización", command = lambda:todasAlertas(RetornarLocalizacion('provincia'),""))
    btn_OptionOne.pack(pady = 10)    
    btn_OptionTwo = tk.Button(ventanaPrincipal, text = "Listar todas las alertas", command = lambda:todasAlertas('0',""))
    btn_OptionTwo.pack(pady = 10)
    btn_OptionThree = tk.Button(ventanaPrincipal, text = "Mostrar gráficos", command = CrearVentanaSecundaria)
    btn_OptionThree.pack(pady = 10)
    btn_OptionFour = tk.Button(ventanaPrincipal, text = "Pronóstico extendido y alertas", command = CrearVentanaCiudad)
    btn_OptionFour.pack(pady = 10)
    btn_OptionFive = tk.Button(ventanaPrincipal, text = "Analizar imagen", command=ViewMethods.MostrarAlertas)
    btn_OptionFive.pack(pady = 10)
    tk.Label(ventanaPrincipal, text = f"Ciudad actual:\n{RetornarLocalizacion('ciudad')}").pack()
    tk.mainloop()

def CrearVentanaSecundaria():
    ventanaSecundaria = tk.Tk()
    ventanaSecundaria.geometry("300x400")
    ventanaSecundaria.title("Seleccione una opción")
    etiquetaArchivo = tk.Label(ventanaSecundaria, text = "Seleccione el archivo csv")
    etiquetaArchivo.pack(pady = 10)
    entradaArchivo = tk.Entry(ventanaSecundaria)
    entradaArchivo.pack()
    btnAbrir = tk.Button(ventanaSecundaria, text = "Seleccionar", command = lambda:entradaArchivo.insert(0,ViewMethods.seleccionarArchivoCsv()))
    btnAbrir.pack()
    etiquetaPeriodo = tk.Label(ventanaSecundaria, text = "Ingrese el período en años a graficar")
    etiquetaPeriodo.pack(pady = 10)
    entradaPeriodo = tk.Entry(ventanaSecundaria)
    entradaPeriodo.pack()
    btn_OptionOne = tk.Button(ventanaSecundaria, text = "Promedio de temperaturas anuales", command = lambda:ViewMethods.crearGraficoTemperaturas(ViewMethods.crearCsvDataFrame(entradaArchivo.get()), entradaPeriodo.get()))
    btn_OptionOne.pack(pady = 10)  
    btn_OptionTwo = tk.Button(ventanaSecundaria, text = "Promedio de humedad", command = lambda:ViewMethods.crearGraficoHumedad(ViewMethods.crearCsvDataFrame(entradaArchivo.get()), entradaPeriodo.get()))
    btn_OptionTwo.pack(pady = 10)  
    btn_OptionThree = tk.Button(ventanaSecundaria, text = "Milímetros máximos de lluvia", command= lambda : ViewMethods.ShowMaxValues(ViewMethods.crearCsvDataFrame(entradaArchivo.get()), 'Precipitation', 'Milímetros máximos de lluvia', entradaPeriodo.get()))
    btn_OptionThree.pack(pady = 10)  
    btn_OptionFour = tk.Button(ventanaSecundaria, text = "Temperatura máxima", command= lambda : ViewMethods.ShowMaxValues(ViewMethods.crearCsvDataFrame(entradaArchivo.get()), 'Max Temperature', 'Temperatura máxima (en °C)', entradaPeriodo.get()))
    btn_OptionFour.pack(pady = 10)
    tk.mainloop()

def CrearVentanaCiudad():
    ventanaCiudad = tk.Tk()
    ventanaCiudad.geometry("300x300")
    etiquetaCiudad = tk.Label(ventanaCiudad, text = "Ingrese ciudad")
    etiquetaCiudad.pack(pady = 10)
    entradaCiudad = tk.Entry(ventanaCiudad)
    entradaCiudad.pack(pady = 10)
    btnBuscar = tk.Button(ventanaCiudad, text = "Buscar", command = lambda:verPronostico(entradaCiudad.get()))
    btnBuscar.pack()
    tk.mainloop()

def main():
    CrearVentanaPrincipal()

if __name__ == "__main__":
    main()