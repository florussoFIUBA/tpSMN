import tkinter as tk
import ViewMethods
import LocationMethods

def CreateMainWindow():
    mainWindow = tk.Tk()
    mainWindow.geometry("300x340")
    mainWindow.title("Tormenta")
    tk.Label(mainWindow, text="Bienvenidos a Tormenta").pack()
    btn_OptionOne = tk.Button(mainWindow, text = "Listar alertas por localización")
    btn_OptionOne.pack(pady = 10)    
    btn_OptionTwo = tk.Button(mainWindow, text = "Listar todas las alertas")
    btn_OptionTwo.pack(pady = 10)
    btn_OptionThree = tk.Button(mainWindow, text = "Mostrar gráficos", command = CreateSecondaryWindow)
    btn_OptionThree.pack(pady = 10)
    btn_OptionFour = tk.Button(mainWindow, text = "Pronóstico extendido y alertas")
    btn_OptionFour.pack(pady = 10)
    btn_OptionFive = tk.Button(mainWindow, text = "Analizar imagen", command=ViewMethods.ShowAlerts)
    btn_OptionFive.pack(pady = 10)
    tk.Label(mainWindow, text = f"Ciudad actual:\n{LocationMethods.ReturnAddress()}").pack()
    tk.mainloop()
#GRAPHICS WINDOW
def CreateSecondaryWindow():
    secondaryWindow = tk.Tk()
    secondaryWindow.geometry("300x200")
    secondaryWindow("Seleccione una opción")
    btn_OptionOne = tk.Button(secondaryWindow, text = "Promedio de temperaturas anuales (5 años)")
    btn_OptionOne.pack(pady = 10)  
    btn_OptionTwo = tk.Button(secondaryWindow, text = "Promedio de humedad (5 años)")
    btn_OptionTwo.pack(pady = 10)  
    btn_OptionThree = tk.Button(secondaryWindow, text = "Milímetros máximos de lluvia (5 años)", command= lambda : ViewMethods.ShowMaxValues('Unemployment_Rate', "Milímetros máximos de lluvia"))
    btn_OptionThree.pack(pady = 10)  
    btn_OptionFour = tk.Button(secondaryWindow, text = "Temperatura máxima (5 años)")
    btn_OptionFour.pack(pady = 10)
    tk.mainloop()

def main():
    CreateMainWindow()

if __name__ == "__main__":
    main()