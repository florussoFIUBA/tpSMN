import cv2
import pandas as pd
import LocationMethods
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
from PIL import Image
import matplotlib
import matplotlib.pyplot as plt
import os
import datetime
import MainMenu
import numpy as np


DEFAULT_EXTENSIONS = (
    ("PNG files", "*.png"),
    ("JPG files", "*.jpg"),
    ("BMP files", "*.bmp"),
    ("JPEG files", "*.jpeg")
)

DEFAULT_LOCATIONS = [
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
DEFAULT_CSV_EXTENSIONS = (
    ("CSV files", "*.csv"),
    
)
def RecortarImagen(imagePath):
    '''Recorta la imagen que se trae por path
    Pre: Recibe el path de una imagen
    Post: Retorna la imagen recortada y convertida a RGB
    '''
    image = cv2.imread(imagePath)
    croppedImage = image[15:555, 21:755]
    return cv2.cvtColor(croppedImage, cv2.COLOR_BGR2RGB)

def DetectarColor(rgbColor):
    '''Detecta si el color está en el rango de los rojos o púrpuras y devuelve el pronóstico correspondiente
    Pre: Recibe un color en formato RGB
    Post: Devuelve el pronóstico o una string vacía en caso de no encontrarlo o de que el color sea nulo
    '''
    try:
        if(rgbColor!='T'):
            if(rgbColor[2]>-1 and rgbColor[2]<101 and rgbColor[1]>-1 and rgbColor[1]<101 and rgbColor[0]>149):
                return "TORMENTAS DE MUCHA LLUVIA"
            elif(rgbColor[2]>149 and rgbColor[1]>-1 and rgbColor[1]<101 and rgbColor[0]>149):
                return "TORMENTAS FUERTES CON GRANIZO"
        return ""
    except Exception as ex:
        messagebox.showerror("Error", ex)
        return ""

def RetornarLocalizacion(x, y):
    '''Devuelve la zona específicada en la constante a través de una comparación en rangos de coordenadas
    Pre: Recibe las coordenadas x y
    Post: Devuelve la zona o en caso de no encontrarla, devuelve Zona desconocida
    '''
    for region in DEFAULT_LOCATIONS:
        if((x>region[1] and x<region[2]) and (y>region[3] and y<region[4])):
            return region[0]
    return "Zona desconocida" 

def TraerAlertas(image):
    '''Retorna las alertas en un string formateado
    Pre: Recibe una imagen en formato array
    Post: Devuelve una string conteniendo las alertas en las distintas zonas
    '''
    try:
        pronosticosTotales = []
        imgToPil = Image.fromarray(image).convert('RGB')
        width, height = imgToPil.size
        for x in range(width):
            for y in range(height):
                currentColor = imgToPil.getpixel((x, y))
                pronostico = DetectarColor(currentColor)
                if (pronostico != ""):
                    location = RetornarLocalizacion(x, y)
                    pronosticoZona = f"{pronostico} en {RetornarLocalizacion(x, y)}"
                    if(pronosticoZona not in pronosticosTotales):
                        pronosticosTotales.append(pronosticoZona)
        return '\n'.join(pronosticosTotales)
    except Exception as ex:
        return ex

'''
Crea dataFramework con los datos del archivo csv
'''
def crearCsvDataFrame(archivo):
    df = pd.read_csv(archivo, index_col=False)
    return df


def ReturnInfo(csvDataFrame, columnToSearch, period):
    csvDataFrame['Date'] = pd.to_datetime(csvDataFrame.Date)
    pastYears = csvDataFrame.set_index('Date').last(period)
    return pastYears[columnToSearch].max()

def ShowMaxValues(df, columnName, dataType, periodo):
    '''Imprime la información basado en un dataframe, nombre de columba y período en años
    '''
    periodo = str(periodo)+"Y"
    messagebox.showinfo(message=f"{dataType}: {ReturnInfo(df, columnName, periodo)}")

'''
Muestra grafico con el promedio de temperaturas maximas y minimas anuales durante
el periodo de tiempo especificado por (periodo)
'''
def crearGraficoTemperaturas(df, ultimosAnios):
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
    
   
'''
Show average yearly humidity values' plot of the last (lastYears) years, from (lastYears)
to (fechaHoy) year, with the dataFramework (df) information
'''

def crearGraficoHumedad(df, ultimosAnios):
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


def MostrarAlertas():
    '''Pide al usuario seleccionar un archivo de imagen, luego ejecuta el proceso y muestra las alertas para la imagen de radar ingresada
    '''
    imagePath = filedialog.askopenfilename(title="Seleccione la imagen a analizar", filetypes=DEFAULT_EXTENSIONS)
    while len(imagePath) == 0:
        messagebox.showerror("Error", "Debe ingresar un archivo para procesar.")
        imagePath = filedialog.askopenfilename(title="Seleccione la imagen a analizar", filetypes=DEFAULT_EXTENSIONS)
    messagebox.showinfo("Alertas",TraerAlertas(RecortarImagen(imagePath)))


def seleccionarArchivoCsv():
    csvDireccion = filedialog.askopenfilename(title="Seleccione el archivo csv", filetypes=DEFAULT_CSV_EXTENSIONS)
    while (len(csvDireccion) == 0 or (os.getcwd() != os.path.dirname(os.path.abspath(csvDireccion))) ):
        messagebox.showerror("Error", "Debe ingresar un archivo para procesar\nDebe estar en la misma carpeta que el archivo de programa")
        csvDireccion = filedialog.askopenfilename(title="Seleccione el archivo csv a analizar", filetypes=DEFAULT_CSV_EXTENSIONS)

    return os.path.basename(csvDireccion)

