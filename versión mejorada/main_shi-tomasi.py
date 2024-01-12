from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import cv2
from PIL import Image, ImageTk
import imutils
import asignacion as asi
import shitomasi

#
#import mysql.connector
import numpy as np

tupla_esquinas = []
var_umbr = int(120)
var_ruido= int(1)
#mi_conexion=mysql.connector.connect(host = '146.83.198.35', user = 'ponate', passwd = 'pedro2023', db = 'pedroo_bd')
#cur = mi_conexion.cursor()
#cur.execute("SHOW TABLES")
#for nombre in cur.fetchall():
#    print(nombre)

def mostrar_en_ventana():
    global image
    global var_umbr
    global var_ruido
    global thresh
    image = cv2.imread(path_image)
    image = imutils.resize(image, width = 600, height = 250)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    imagen = cv2.GaussianBlur(image, (5, 5), 0)
    ret, thresh = cv2.threshold(image, var_umbr, 255, 0)
    thresh = cv2.medianBlur(thresh, var_ruido)
    image = Image.fromarray(imagen)

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
    global tupla_esquinas
    tupla_esquinas = []
    path_image = filedialog.askopenfilename(filetypes = [
        ("image", ".jpeg"),
        ("image", ".png"),
        ("image", ".jpg")])
    imagen_color = cv2.imread(path_image)   
    image = cv2.cvtColor(imagen_color, cv2.COLOR_BGR2GRAY)
    imagen = cv2.GaussianBlur(image, (5, 5), 0)
    dst = cv2.cornerHarris(imagen,64,31,0.21)
    dst = cv2.dilate(dst,None)
    
    #image = imutils.resize(dst, width = 600, height = 250)
 
   
    ret, dst = cv2.threshold(dst,0.01*dst.max(),255,0)
    dst = np.uint8(dst)
    
    ret, labels, stats, centroids = cv2.connectedComponentsWithStats(dst)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 0.3)
    corners = cv2.cornerSubPix(imagen,np.float32(centroids),(5,5),(-1,-1),criteria)
    #print(corners)
    #for corner in corners:     
    #    x,y = corner.ravel()
    #    x = int(x)
    #    y = int(y)
    #    #print(x,y)
        #cv2.circle(imagen_color, (x,y), 15, 255, -1)
    #    tupla_esquinas.append((x,y))

    #print(tupla_esquinas)
    image = imutils.resize(imagen_color, width = 600, height = 250)
    #canny = cv2.Canny(imagen, 30, 150)
    ret, thresh = cv2.threshold(image, 120, 255, 0)
    img = Image.fromarray(image)
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
    global tupla_esquinas
    label_imagen_procesada = ttk.Label(root)
    imagen_normal = cv2.imread(path_image)
    primera_esquina = asi.esquina_sup_izq(tupla_esquinas)
    lista_ordenada = []
    list = []
    list.append(primera_esquina)
    lista_ordenada = asi.asignar_orden_a_puntos(tupla_esquinas, primera_esquina, list, 'hacia el lado')
    print(lista_ordenada)
    print(primera_esquina)
    #cv2.circle(imagen_normal, primera_esquina, 15, 150, -1)
    for corner in lista_ordenada:     
        cv2.circle(imagen_normal, corner, 15, 150, -1)

    imagen_normal = imutils.resize(imagen_normal, width = 600, height = 250)

    #im = procesar_imagen(thresh, imagen_normal)
    imagen_normal = Image.fromarray(imagen_normal)
    imagen_normal = ImageTk.PhotoImage(imagen_normal)
    label_imagen_procesada.configure(image=imagen_normal)
    label_imagen_procesada.image = imagen_normal
    label_imagen_procesada.grid(column=2, row=0)


#image = None
root = Tk()
root.title("Ventana principal")
#root.state('zoomed')
testWidget = shitomasi.Page(root, root) #una instancia de la clase Page, con parámetros root, la ventana que se acaba de crear.Page hereda elementos de un widget Frane, y se lemañaden algunos elementos más en la  definición de clase
testWidget.grid(row=0, column=1, sticky="W")
#btn = Button(root, text="Elegir imagen", width=25, command=elegir_imagen)
#btn.grid(column=0, row=0, padx=5, pady=5) 

root.mainloop()

