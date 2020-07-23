import tkinter as tk
import ViewMethods
import LocationMethods



def CrearVentanaPrincipal():
    mainWindow = tk.Tk()
    mainWindow.geometry("300x340")
    mainWindow.title("Tormenta")
    tk.Label(mainWindow, text="Bienvenidos a Tormenta").pack()
    btn_OptionOne = tk.Button(mainWindow, text = "Listar alertas por localización")
    btn_OptionOne.pack(pady = 10)    
    btn_OptionTwo = tk.Button(mainWindow, text = "Listar todas las alertas")
    btn_OptionTwo.pack(pady = 10)
    btn_OptionThree = tk.Button(mainWindow, text = "Mostrar gráficos", command = CrearVentanaSecundaria)
    btn_OptionThree.pack(pady = 10)
    btn_OptionFour = tk.Button(mainWindow, text = "Pronóstico extendido y alertas")
    btn_OptionFour.pack(pady = 10)
    btn_OptionFive = tk.Button(mainWindow, text = "Analizar imagen", command=ViewMethods.MostrarAlertas)
    btn_OptionFive.pack(pady = 10)
    tk.Label(mainWindow, text = f"Ciudad actual:\n{LocationMethods.ReturnAddress()}").pack()
    tk.mainloop()

def CrearVentanaSecundaria():
    secondaryWindow = tk.Tk()
    secondaryWindow.geometry("300x300")
    secondaryWindow.title("Seleccione una opción")
    etiquetaArchivo = tk.Label(secondaryWindow, text = "Seleccione el archivo csv")
    etiquetaArchivo.pack(pady = 10)
    entradaArchivo = tk.Entry(secondaryWindow)
    entradaArchivo.pack()
    btnAbrir = tk.Button(secondaryWindow, text = "Seleccionar", command = lambda:entradaArchivo.insert(0,ViewMethods.seleccionarArchivoCsv()))
    btnAbrir.pack()
    etiquetaPeriodo = tk.Label(secondaryWindow, text = "Ingrese el período en años a graficar")
    etiquetaPeriodo.pack(pady = 10)
    entradaPeriodo = tk.Entry(secondaryWindow)
    entradaPeriodo.pack()
    btn_OptionOne = tk.Button(secondaryWindow, text = "Promedio de temperaturas anuales", command = lambda:ViewMethods.crearGraficoTemperaturas(ViewMethods.crearCsvDataFrame(entradaArchivo.get()), entradaPeriodo.get()))
    btn_OptionOne.pack(pady = 10)  
    btn_OptionTwo = tk.Button(secondaryWindow, text = "Promedio de humedad", command = lambda:ViewMethods.crearGraficoHumedad(ViewMethods.crearCsvDataFrame(entradaArchivo.get()), entradaPeriodo.get()))
    btn_OptionTwo.pack(pady = 10)  
    btn_OptionThree = tk.Button(secondaryWindow, text = "Milímetros máximos de lluvia", command= lambda : ViewMethods.ShowMaxValues(ViewMethods.crearCsvDataFrame(entradaArchivo.get()), 'Precipitation', 'Milímetros máximos de lluvia', entradaPeriodo.get()))
    btn_OptionThree.pack(pady = 10)  
    btn_OptionFour = tk.Button(secondaryWindow, text = "Temperatura máxima", command= lambda : ViewMethods.ShowMaxValues(ViewMethods.crearCsvDataFrame(entradaArchivo.get()), 'Max Temperature', 'Temperatura máxima (en °C)', entradaPeriodo.get()))
    btn_OptionFour.pack(pady = 10)
    tk.mainloop()

def main():
    CrearVentanaPrincipal()

if __name__ == "__main__":
    main()