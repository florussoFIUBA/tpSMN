import cv2
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image

DEFAULT_EXTENSIONS = (
    ("All supported files", "*.jpg,*.png,*.bmp,*.jpeg"),
    ("JPG files", "*.jpg"),
    ("PNG files", "*.png"),
    ("BMP files", "*.bmp"),
    ("JPEG files", "*.jpeg")
)
DEFAULT_PRONOSTICS = [
    ("ALERTA: TORMENTAS DE MUCHA LLUVIA",[(238, 17, 51),(204, 0, 17), (170,0,17), (153, 0, 0)]),
    ("ALERTA: TORMENTAS FUERTES CON GRANIZO",[(187, 0, 2),(221, 0, 153), (238,0,238), (204, 0, 204), (170, 0, 187), (153, 0, 153), (255, 255, 255), (238, 238, 238), (204,238,238), (170,238,204), (153, 221, 204), (136, 221, 187)])
]

def CropImage(imagePath):
    image = cv2.imread(imagePath)
    croppedImage = image[15:555, 21:755]
    return croppedImage

def ReturnColorNames(mainColors):
    for colorDict in mainColors:
        for colorList in DEFAULT_PRONOSTICS:
            if(colorList[1].count(colorDict[1])>0):
                print(colorList[0])

def ReturnMainColors(image):
    imgToPil = Image.fromarray(image)
    return imgToPil.getcolors()

def main():
    imagePath = filedialog.askopenfilename(title="Seleccione la imagen a analizar", filetypes=DEFAULT_EXTENSIONS)
    while len(imagePath) == 0:
        messagebox.showerror("Error", "Debe ingresar un archivo para procesar.")
        imagePath = filedialog.askopenfilename(title="Seleccione la imagen a analizar", filetypes=DEFAULT_EXTENSIONS)
    ReturnColorNames(ReturnMainColors(CropImage(imagePath)))

if __name__ == "__main__":
    main()

