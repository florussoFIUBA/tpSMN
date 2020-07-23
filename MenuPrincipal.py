import tkinter as tk
import ViewMethods
import MetodosLocalizacion
import GeolocalizacionAlertas
import Mostrar_Alertas
import PronosticoExtendido

def CrearVentanaPrincipal():
    ventanaPrincipal = tk.Tk()
    ventanaPrincipal.geometry("300x340")
    ventanaPrincipal.title("Tormenta")
    tk.Label(ventanaPrincipal, text="Bienvenidos a Tormenta").pack()
    btn_OptionOne = tk.Button(ventanaPrincipal, text = "Listar alertas por localización", command = GeolocalizacionAlertas.mostrarAlertas)
    btn_OptionOne.pack(pady = 10)    
    btn_OptionTwo = tk.Button(ventanaPrincipal, text = "Listar todas las alertas", command = Mostrar_Alertas.todasAlertas)
    btn_OptionTwo.pack(pady = 10)
    btn_OptionThree = tk.Button(ventanaPrincipal, text = "Mostrar gráficos", command = CrearVentanaSecundaria)
    btn_OptionThree.pack(pady = 10)
    btn_OptionFour = tk.Button(ventanaPrincipal, text = "Pronóstico extendido y alertas", command = CrearVentanaCiudad)
    btn_OptionFour.pack(pady = 10)
    btn_OptionFive = tk.Button(ventanaPrincipal, text = "Analizar imagen", command=ViewMethods.MostrarAlertas)
    btn_OptionFive.pack(pady = 10)
    tk.Label(ventanaPrincipal, text = f"Ciudad actual:\n{MetodosLocalizacion.RetornarLocalizacion()}").pack()
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
    btnBuscar = tk.Button(ventanaCiudad, text = "Buscar", command = lambda:PronosticoExtendido.mostrarData(entradaCiudad.get()))
    btnBuscar.pack()
    tk.mainloop()

def main():
    CrearVentanaPrincipal()

if __name__ == "__main__":
    main()