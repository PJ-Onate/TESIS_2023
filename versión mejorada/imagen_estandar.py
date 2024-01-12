from PIL import ImageTk
import PIL.Image
from tkinter import *
from tkinter import ttk

def mostrar_img_dimension_estandar(root, frame):
    ventana_imagen = Toplevel(root)
    #window.geometry("800x800")
    imagen = PIL.Image.open('C:/Users/Peter/Desktop/PJ/prueba_opencv.png')
    imagen = imagen.resize((500,500))

    img = ImageTk.PhotoImage(imagen)
    label = ttk.Label(ventana_imagen, image=img)
    label.grid(row=0, column=1)
 
    
    
