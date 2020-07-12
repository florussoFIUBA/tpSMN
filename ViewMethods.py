import cv2
import pandas as pd
import LocationMethods
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image
import matplotlib
import MainMenu


DEFAULT_EXTENSIONS = (
    ("PNG files", "*.png"),
    ("JPG files", "*.jpg"),
    ("BMP files", "*.bmp"),
    ("JPEG files", "*.jpeg")
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

def ReturnInfo(csvDataFrame, columnToSearch, period):
    csvDataFrame['Date'] = pd.to_datetime(csvDataFrame.Date)
    pastYears = csvDataFrame.set_index('Date').last(period)
    return pastYears[columnToSearch].max()

def ShowMaxValues(columnName, dataType):
    ##THIS WILL BE REPLACED WITH CSV PARSING METHOD
    Data = {'Date': ['2017-04-03','2020-04-03','2019-04-03','2018-04-03','2016-04-03','2015-04-03','2014-04-03','2013-04-03','2012-04-03','2011-04-03'],
        'Unemployment_Rate': [9.8,12,8,7.2,6.9,7,6.5,6.2,5.5,6.3]
       }
    df = pd.DataFrame(Data,columns=['Date','Unemployment_Rate'])
    messagebox.showinfo(message=f"{dataType}: {ReturnInfo(df, columnName, '5Y')}")

def ShowAlerts():
    imagePath = filedialog.askopenfilename(title="Seleccione la imagen a analizar", filetypes=DEFAULT_EXTENSIONS)
    while len(imagePath) == 0:
        messagebox.showerror("Error", "Debe ingresar un archivo para procesar.")
        imagePath = filedialog.askopenfilename(title="Seleccione la imagen a analizar", filetypes=DEFAULT_EXTENSIONS)
    messagebox.showinfo("Alertas",ReturnAlerts(ReturnMainColors(CropImage(imagePath))))



