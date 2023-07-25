from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import cv2
from PIL import Image, ImageTk
import imutils
from proces import procesar_imagen

var_umbr = int(120)
var_ruido= int(1)

def mostrar_en_ventana():
    global image
    global var_umbr
    global var_ruido
    global thresh
    image = cv2.imread(path_image)
    image = imutils.resize(image, width = 600, height = 250)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(image, var_umbr, 255, 0)
    thresh = cv2.medianBlur(thresh, var_ruido)
    image = Image.fromarray(thresh)

    img = ImageTk.PhotoImage(image)

    label = ttk.Label(root, image = img)
    label.configure(image = img)#con estas lineas...
    label.image = img#
    label.grid(column=1, row=0)

def limite_inf_umbr(val1):
    global var_umbr
    var_umbr = int(val1)
    mostrar_en_ventana()

def ruido(val2):
    global var_ruido
    var_ruido = int(val2)
    mostrar_en_ventana()

path_image = ""
def elegir_imagen():
    global image
    global path_image
    global thresh
    path_image = filedialog.askopenfilename(filetypes = [
        ("image", ".jpeg"),
        ("image", ".png"),
        ("image", ".jpg")])
    image = cv2.imread(path_image)
    image = imutils.resize(image, width = 600, height = 250)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(image, 120, 255, 0)
    img = Image.fromarray(thresh)
    img = ImageTk.PhotoImage(img)

    label = ttk.Label(root, image = img)
    label.configure(image = img)#con estas lineas...
    label.image = img#
    label.grid(column=1, row=0)
    marcador1 = Scale(root, orient='horizontal', from_=0, to=255, length=400, command=limite_inf_umbr)
    marcador2 = Scale(root, orient='horizontal', from_=1, to=39, length=400, command=ruido)
    Label(root, text="Umbralización").grid(row=1, column=1)
    marcador1.grid(row=2, column=1)
    Label(root, text="Ruido").grid(row=3, column=1)
    marcador2.grid(row=4, column=1)
    boton_intersecciones = ttk.Button(root, text="Procesar imagen", command=proc)
    boton_intersecciones.grid(row=5, column=1)

def proc():
    global thresh
    global path_image
    label_imagen_procesada = ttk.Label(root)
    imagen_normal = cv2.imread(path_image)
    imagen_normal = imutils.resize(imagen_normal, width = 600, height = 250)

    im = procesar_imagen(thresh, imagen_normal)
    imagen_normal = Image.fromarray(im)
    imagen_normal = ImageTk.PhotoImage(imagen_normal)
    label_imagen_procesada.configure(image=imagen_normal)
    label_imagen_procesada.image = imagen_normal
    label_imagen_procesada.grid(column=2, row=0)

#image = None
root = Tk()
root.title("Ventana principal")
root.state('zoomed')
btn = Button(root, text="Elegir imagen", width=25, command=elegir_imagen)
btn.grid(column=0, row=0, padx=5, pady=5) 

root.mainloop()

