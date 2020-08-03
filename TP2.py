import tkinter as tk
import json
import requests
import geocoder
import tkinter.scrolledtext as tkscrolled
import cv2
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import os
import datetime
import numpy as np
from geopy.geocoders import Nominatim
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
from PIL import Image

PRONOSTICO1D = "https://ws.smn.gob.ar/map_items/forecast/1"
PRONOSTICO2D = "https://ws.smn.gob.ar/map_items/forecast/2"
PRONOSTICO3D = "https://ws.smn.gob.ar/map_items/forecast/3"
ALERTAS_URL = "https://ws.smn.gob.ar/alerts/type/AL"
EXTENSIONES_IMG = (
    ("PNG files", "*.png"),
)
UBICACIONES_POR_DEFECTO = [
    ["SANTA FE - PARANA", 426, 565, 42, 180],
    ["CORDOBA", 319, 422, 54, 187],
    ["SAN LUIS", 259, 318, 54, 126],
    ["MENDOZA", 158, 253, 158, 296],
    ["NEUQUEN", 134, 224, 356, 456],
    ["SANTA ROSA", 230, 387, 298, 358],
    ["SANTA FE - MERCEDES", 445, 636, 0, 38],
    ["SANTA FE - PERGAMINO", 455, 533, 235, 280],
    ["CABA - LA PLATA - GBA", 506, 585, 235, 280],
    ["BAHIA BLANCA", 388, 446, 381, 438],
    ["VIEDMA", 362, 455, 451, 502]
]
EXTENSIONES_CSV = (
    ("CSV files", "*.csv"),
)
headers = {'Content-Type':'application/json',
            'Authorization':''}

def RecortarImagen(rutaImagen):
    '''Recorta la imagen que se trae por path
    Pre: Recibe el path de una imagen
    Post: Retorna la imagen recortada y convertida a RGB
    '''
    try:
        imagen = cv2.imread(rutaImagen)
        imagenRecortada = imagen[15:555, 21:755]
        return cv2.cvtColor(imagenRecortada, cv2.COLOR_BGR2RGB)
    except Exception as ex:
        return ex        

def DetectarColor(colorRgb):
    '''Detecta si el color está en el rango de los rojos o púrpuras y devuelve el pronóstico correspondiente
    Pre: Recibe un color en formato RGB
    Post: Devuelve el pronóstico o una string vacía en caso de no encontrarlo o de que el color sea nulo
    '''
    try:
        if(colorRgb!='T'):
            if(colorRgb[2]>-1 and colorRgb[2]<101 and colorRgb[1]>-1 and colorRgb[1]<101 and colorRgb[0]>149):
                return "TORMENTAS DE MUCHA LLUVIA"
            elif(colorRgb[2]>149 and colorRgb[1]>-1 and colorRgb[1]<101 and colorRgb[0]>149):
                return "TORMENTAS FUERTES CON GRANIZO"
        return ""
    except Exception as ex:
        messagebox.showerror("Error", ex)
        return ""

def RetornarLocalizacionDePixels(x, y):
    '''Devuelve la zona específicada en la constante a través de una comparación en rangos de coordenadas
    Pre: Recibe las coordenadas x y
    Post: Devuelve la zona o en caso de no encontrarla, devuelve Zona desconocida
    '''
    for region in UBICACIONES_POR_DEFECTO:
        if((x>region[1] and x<region[2]) and (y>region[3] and y<region[4])):
            return region[0]
    return "Zona desconocida" 

def TraerAlertasDeImagen(imagen):
    '''Retorna las alertas en un string formateado
    Pre: Recibe una imagen en formato array
    Post: Devuelve una string conteniendo las alertas en las distintas zonas
    '''
    try:
        if(not isinstance(imagen, Exception)):
            pronosticosTotales = []
            imgToPil = Image.fromarray(imagen).convert('RGB')
            width, height = imgToPil.size
            for x in range(width):
                for y in range(height):
                    currentColor = imgToPil.getpixel((x, y))
                    pronostico = DetectarColor(currentColor)
                    if (pronostico != ""):
                        location = RetornarLocalizacionDePixels(x, y)
                        pronosticoZona = f"{pronostico} en {RetornarLocalizacionDePixels(x, y)}"
                        if(pronosticoZona not in pronosticosTotales):
                            pronosticosTotales.append(pronosticoZona)
            return '\n'.join(pronosticosTotales)
        else:
            return imagen
    except Exception as ex:
        return ex


def CrearCsvDataFrame(archivo):
    '''Crea dataFramework con los datos del archivo csv
    PRE: Recive el path de un archivo CSV
    POST: Devuelve un dataframe con la información del archivo
    '''
    df = pd.read_csv(archivo, index_col=False)
    return df

def RetornarInformacionCsv(csvDataFrame, nombreColumna, periodo):
    '''
    PRE: Recibe un dataframe, la columna por la cual va a buscar la información y el período expresado en años
    POST: Devuelve el valor máximo
    '''
    try:
        csvDataFrame['Date'] = pd.to_datetime(csvDataFrame.Date)
        pastYears = csvDataFrame.set_index('Date').last(periodo)
        return pastYears[nombreColumna].max()
    except Exception as ex:
       return ex

def SeleccionarArchivoCsv():
    '''Abre un open file dialog para que el usuario seleccione un archivo csv
    POST: Retorna el path del archivo csv
    '''
    csvDireccion = filedialog.askopenfilename(title="Seleccione el archivo csv", filetypes=EXTENSIONES_CSV)
    while (len(csvDireccion) == 0 or (os.getcwd() != os.path.dirname(os.path.abspath(csvDireccion))) ):
        messagebox.showerror("Error", "Debe ingresar un archivo para procesar\nDebe estar en la misma carpeta que el archivo de programa")
        csvDireccion = filedialog.askopenfilename(title="Seleccione el archivo csv a analizar", filetypes=EXTENSIONES_CSV)

    return os.path.basename(csvDireccion)

def ObtenerSMNjson(url):
    '''Recibe un link url, y devuelve un archivo Json "crudo".
    '''
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        rawJson = json.loads(response.content.decode('utf-8'))
        return json.dumps(rawJson, sort_keys=True, indent=4, default=rawJson)
    else:
        return None
    
def ObtenerObjetoJSON(url):
    '''Recibe un Json "crudo" y lo devuelve como un objeto Json para que pueda ser abierto e interpretado facilmente.
    '''
    info = ObtenerSMNjson(url)
    
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
        txtBoxWidth, txtBoxHeight = 200, 200
        ventanaAlertas = tk.Tk()
        ventanaAlertas.geometry("250x250")
        ventanaAlertas.title("Alertas")
        txtBoxScroll = tkscrolled.ScrolledText(master = ventanaAlertas, width = txtBoxWidth, height = txtBoxHeight, wrap='word')
        txtBoxScroll.insert(index = 1.0, chars = texto)
        txtBoxScroll.pack()
        ventanaAlertas.mainloop()
    else:
        messagebox.showinfo("Alertas", "No se registraron alertas")

def ObtenerURL():
    '''Crea una lista con los jsons de los pronosticos para cada dia, para poder iterar cada dia de pronosticos en la funcion VerPronostico.
    '''
    lista_url = []
    un_dia = ObtenerObjetoJSON(PRONOSTICO1D)
    dos_dias = ObtenerObjetoJSON(PRONOSTICO2D)
    tres_dias = ObtenerObjetoJSON(PRONOSTICO3D)
    lista_url = [un_dia,dos_dias,tres_dias]
    return lista_url

def TodasAlertas(provincia,alertasStr):
    '''Recibe una provincia
    Devuelve en pantalla las alertas que involucran la provincia.
    Si se recibe '0' como provincia, muestra todas las alertas sin filtrar.
    '''
    alertas = ObtenerObjetoJSON(ALERTAS_URL)
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

def VerPronostico(ciudad):
    '''Recibe una ciudad ingresada por el usuario.
    En caso de encontrar la ciudad en la base de datos, devuelve en pantalla el pronostico extendido para esa ciudad, y llama a la funcion de verAlertas con la provincia donde se encuentra la ciudad.
    '''
    lista_url = ObtenerURL()
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
    TodasAlertas(provincia,alertasStr)
        
def RetornarLocalizacionActual():
    '''Usando la libreria geocoder, devuelve una geolocalizacion (lat long).
    '''
    myLocation = geocoder.ip('me')
    return myLocation.latlng

def RetornarLocalizacion(indice):
    '''En la lista location.address de geolocator, devuelve el elemento cuyo indice es el parametro.
    '''
    try:
        latLong = RetornarLocalizacionActual()
        geolocator = Nominatim(user_agent="tp2")
        location = geolocator.reverse(f"{latLong[0]}, {latLong[1]}")
        localidad = location.address.split(',')[indice]
        usuario_lista = []
        for i in localidad:
            usuario_lista.append(i)
        usuario_lista.remove(" ")
        localidad = "".join(usuario_lista)
        return localidad
    except Exception as ex:
        return ex
    
def MostrarValoresMaximos(df, nombreColumna, tipoDato, periodo):
    '''Muestra la información basado en un dataframe, nombre de columba y período en años
    PRE: Recibe un dataframe, la columna por la cual va a buscar, el tipo de dato y el período expresado en años
    '''
    periodo = str(periodo)+"Y"
    messagebox.showinfo(message=f"{tipoDato}: {RetornarInformacionCsv(df, nombreColumna, periodo)}")


def CrearGraficoTemperaturas(df, ultimosAnios):
    '''
    Muestra grafico con el promedio de temperaturas maximas y minimas anuales durante
    el periodo de tiempo especificado por (periodo)
    '''
    try:
        listaAnio=[]
        listaTempMax=[]
        listaTempMin=[]
        ultimosAnios=int(ultimosAnios)
        df['Date'] = pd.to_datetime(df['Date']).dt.date
        fechaHoy=(pd.to_datetime('today')).date()
        for i in range(ultimosAnios, -1, -1):
            
            fechaInicio=fechaHoy.replace(year=fechaHoy.year-i, month=1, day =1)
            fechaFin=fechaHoy.replace(year=fechaHoy.year-i, month=12, day=31)
            listaAnio.append(fechaInicio.year)
            listaTempMax.append(df.loc[((df['Date']<=fechaFin) & (df['Date']>=fechaInicio)), 'Max Temperature'].mean())
            listaTempMin.append(df.loc[((df['Date']<=fechaFin) & (df['Date']>=fechaInicio)), 'Min Temperature'].mean())
        dfPromedioTemp=pd.DataFrame({'Temperatura Maxima':listaTempMax, 'Temperatura Minima':listaTempMin}, index=listaAnio)
        graficoTemperatura=dfPromedioTemp.plot.bar(title='Promedio de temperaturas anuales')
        graficoTemperatura.set_xlabel("Año")
        graficoTemperatura.set_ylabel("Promedio")
        plt.show()
    except Exception as ex:
        messagebox.showerror("Error", ex)


def CrearGraficoHumedad(df, ultimosAnios):
    '''Muestra gráfico de humedad de los últimos años
    PRE: Recibe un dataframe con la información y la cantidad de años a buscar
    '''
    try:
        listaAnio=[]
        listaHumedad=[]
        ultimosAnios=int(ultimosAnios)
        df['Date'] = pd.to_datetime(df['Date']).dt.date
        fechaHoy=(pd.to_datetime('today')).date()
        for i in range(ultimosAnios, -1, -1):
            
            fechaInicio=fechaHoy.replace(year=fechaHoy.year-i, month=1, day =1)
            fechaFin=fechaHoy.replace(year=fechaHoy.year-i, month=12, day=31)
            listaAnio.append(fechaInicio.year)
            listaHumedad.append(df.loc[((df['Date']<=fechaFin) & (df['Date']>=fechaInicio)), 'Relative Humidity'].mean())
        dfPromedioHum=pd.DataFrame({'Promedio humedad':listaHumedad}, index=listaAnio)
        graficoHum=dfPromedioHum.plot.bar(title='Promedio de humedad')
        graficoHum.set_xlabel("Año")
        graficoHum.set_ylabel("Promedio")
        plt.show()
    except Exception as ex:
        messagebox.showerror("Error", ex)

def MostrarAlertasRadar():
    '''Pide al usuario seleccionar un archivo de imagen, luego ejecuta el proceso y muestra las alertas para la imagen de radar ingresada
    '''
    imagePath = filedialog.askopenfilename(title="Seleccione la imagen a analizar", filetypes=EXTENSIONES_IMG)
    while len(imagePath) == 0:
        messagebox.showerror("Error", "Debe ingresar un archivo para procesar.")
        imagePath = filedialog.askopenfilename(title="Seleccione la imagen a analizar", filetypes=EXTENSIONES_IMG)
    messagebox.showinfo("Alertas",TraerAlertasDeImagen(RecortarImagen(imagePath)))

def MenuTormenta():
    ventanaTormenta = tk.Tk()
    ventanaTormenta.geometry("300x340")
    ventanaTormenta.title("Tormenta")
    tk.Label(ventanaTormenta, text="Bienvenidos a Tormenta").pack()
    btn_OpcionUno = tk.Button(ventanaTormenta, text = "Listar alertas por localización", command = lambda:TodasAlertas(RetornarLocalizacion(3),""))
    btn_OpcionUno.pack(pady = 10)    
    btn_OpcionDos = tk.Button(ventanaTormenta, text = "Listar todas las alertas", command = lambda:TodasAlertas('0',""))
    btn_OpcionDos.pack(pady = 10)
    btn_OpcionTres = tk.Button(ventanaTormenta, text = "Mostrar gráficos", command = CrearVentanaEstadisticas)
    btn_OpcionTres.pack(pady = 10)
    btn_OpcionCuatro = tk.Button(ventanaTormenta, text = "Pronóstico extendido y alertas", command = CrearVentanaCiudad)
    btn_OpcionCuatro.pack(pady = 10)
    btn_OptionFive = tk.Button(ventanaTormenta, text = "Analizar imagen", command=MostrarAlertasRadar)
    btn_OptionFive.pack(pady = 10)
    tk.Label(ventanaTormenta, text = RetornarLocalizacion(2)).pack()
    tk.mainloop()

def CrearVentanaEstadisticas():
    ventanaEstadisticas = tk.Tk()
    ventanaEstadisticas.geometry("300x400")
    ventanaEstadisticas.title("Seleccione una opción")
    etiquetaArchivo = tk.Label(ventanaEstadisticas, text = "Seleccione el archivo csv")
    etiquetaArchivo.pack(pady = 10)
    entradaArchivo = tk.Entry(ventanaEstadisticas)
    entradaArchivo.pack()
    btnAbrir = tk.Button(ventanaEstadisticas, text = "Seleccionar", command = lambda:entradaArchivo.insert(0,SeleccionarArchivoCsv()))
    btnAbrir.pack()
    etiquetaPeriodo = tk.Label(ventanaEstadisticas, text = "Ingrese el período en años a graficar")
    etiquetaPeriodo.pack(pady = 10)
    entradaPeriodo = tk.Entry(ventanaEstadisticas)
    entradaPeriodo.pack()
    btn_OpcionUno = tk.Button(ventanaEstadisticas, text = "Promedio de temperaturas anuales", command = lambda:CrearGraficoTemperaturas(CrearCsvDataFrame(entradaArchivo.get()), entradaPeriodo.get()))
    btn_OpcionUno.pack(pady = 10)  
    btn_OpcionDos = tk.Button(ventanaEstadisticas, text = "Promedio de humedad", command = lambda:CrearGraficoHumedad(CrearCsvDataFrame(entradaArchivo.get()), entradaPeriodo.get()))
    btn_OpcionDos.pack(pady = 10)  
    btn_OpcionTres = tk.Button(ventanaEstadisticas, text = "Milímetros máximos de lluvia", command= lambda : MostrarValoresMaximos(CrearCsvDataFrame(entradaArchivo.get()), 'Precipitation', 'Milímetros máximos de lluvia', entradaPeriodo.get()))
    btn_OpcionTres.pack(pady = 10)  
    btn_OpcionCuatro = tk.Button(ventanaEstadisticas, text = "Temperatura máxima", command= lambda : MostrarValoresMaximos(CrearCsvDataFrame(entradaArchivo.get()), 'Max Temperature', 'Temperatura máxima (en °C)', entradaPeriodo.get()))
    btn_OpcionCuatro.pack(pady = 10)
    tk.mainloop()

def CrearVentanaCiudad():
    ventanaCiudad = tk.Tk()
    ventanaCiudad.geometry("300x300")
    etiquetaCiudad = tk.Label(ventanaCiudad, text = "Ingrese ciudad")
    etiquetaCiudad.pack(pady = 10)
    entradaCiudad = tk.Entry(ventanaCiudad)
    entradaCiudad.pack(pady = 10)
    btnBuscar = tk.Button(ventanaCiudad, text = "Buscar", command = lambda:VerPronostico(entradaCiudad.get()))
    btnBuscar.pack()
    tk.mainloop()

def main():
    MenuTormenta()

if __name__ == "__main__":
    main()