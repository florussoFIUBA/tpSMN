import tkinter as tk

def CreateMainWindow():
    mainWindow = tk.Tk()
    mainWindow.geometry("300x500")
    mainWindow.title = "Tormenta"
    tk.Label(mainWindow, text="Bienvenidos a Tormenta").pack()
    btn_OptionOne = tk.Button(mainWindow, text = "Listar alertas por localización")
    btn_OptionOne.pack(pady = 10)    
    btn_OptionTwo = tk.Button(mainWindow, text = "Listar todas las alertas")
    btn_OptionTwo.pack(pady = 10)
    btn_OptionThree = tk.Button(mainWindow, text = "Mostrar gráficos")
    btn_OptionThree.pack(pady = 10)
    btn_OptionFour = tk.Button(mainWindow, text = "Pronóstico extendido y alertas")
    btn_OptionFour.pack(pady = 10)
    btn_OptionFive = tk.Button(mainWindow, text = "Analizar imagen")
    btn_OptionFive.pack(pady = 10)
    tk.mainloop()
    