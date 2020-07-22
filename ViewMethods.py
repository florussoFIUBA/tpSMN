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



DEFAULT_EXTENSIONS = (
    ("PNG files", "*.png"),
    ("JPG files", "*.jpg"),
    ("BMP files", "*.bmp"),
    ("JPEG files", "*.jpeg")
)
DEFAULT_CSV_EXTENSIONS = (
    ("CSV files", "*.csv"),
    
)
DEFAULT_PRONOSTICS = [
    ("TORMENTAS DE MUCHA LLUVIA",[(238, 17, 51),(204, 0, 17), (170,0,17), (153, 0, 0)]),
    ("TORMENTAS FUERTES CON GRANIZO",[(187, 0, 2),(221, 0, 153), (238,0,238), (204, 0, 204), (170, 0, 187), (153, 0, 153), (255, 255, 255), (238, 238, 238), (204,238,238), (170,238,204), (153, 221, 204), (136, 221, 187)])
]

def CropImage(imagePath):
    image = cv2.imread(imagePath)
    croppedImage = image[15:555, 21:755]
    return croppedImage

def ReturnAlerts(mainColors):
    pronostics = ""
    for colorDict in mainColors:
        for colorList in DEFAULT_PRONOSTICS:
            if(colorList[1].count(colorDict[1])>0):
                if(colorList[0] not in pronostics):
                    pronostics+=f"{colorList[0]}\n"
    return pronostics

def ReturnMainColors(image):
    imgToPil = Image.fromarray(image)
    return imgToPil.getcolors()


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
    ##THIS WILL BE REPLACED WITH CSV PARSING METHOD
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


def ShowAlerts():
    imagePath = filedialog.askopenfilename(title="Seleccione la imagen a analizar", filetypes=DEFAULT_EXTENSIONS)
    while len(imagePath) == 0:
        messagebox.showerror("Error", "Debe ingresar un archivo para procesar.")
        imagePath = filedialog.askopenfilename(title="Seleccione la imagen a analizar", filetypes=DEFAULT_EXTENSIONS)
    messagebox.showinfo("Alertas",ReturnAlerts(ReturnMainColors(CropImage(imagePath))))


def seleccionarArchivoCsv():
    csvDireccion = filedialog.askopenfilename(title="Seleccione el archivo csv", filetypes=DEFAULT_CSV_EXTENSIONS)
    while (len(csvDireccion) == 0 or (os.getcwd() != os.path.dirname(os.path.abspath(csvDireccion))) ):
        messagebox.showerror("Error", "Debe ingresar un archivo para procesar\nDebe estar en la misma carpeta que el archivo de programa")
        csvDireccion = filedialog.askopenfilename(title="Seleccione el archivo csv a analizar", filetypes=DEFAULT_CSV_EXTENSIONS)

    return os.path.basename(csvDireccion)

