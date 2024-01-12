import cv2
import imutils
from PIL import Image, ImageTk
from centros import lista_de_centros
import asignacion as asi

var_umbr = 0
img = None
thresh = None

def retoque_img(path):
    global img
    img = cv2.imread(path)
    img = imutils.resize(img, width=600, height=250)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    img = imagen_a_desplegar(img)
    return img
    
def imagen_a_desplegar(frame):
    global var_umbr
    global thresh
    ret, thresh = cv2.threshold(frame, var_umbr, 255, 0)
    imagen = Image.fromarray(thresh)
    imagen = ImageTk.PhotoImage(imagen)
    return imagen
    

def funcionalidad_umbr(val1):
    global var_umbr
    global img
    var_umbr = int(val1)
    img = imagen_a_desplegar(thresh)

def procesar_imagen(frame, normal):
    contornos_imagen, hierarchy = cv2.findContours(frame,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE)
    centros_imagen = lista_de_centros(contornos_imagen)
    centros_imagen.sort
    print(centros_imagen)
    for c in range(len(centros_imagen)):
        cv2.circle(normal, centros_imagen[c], 5, (255,255,255), -1)

    sum = 0
    for c in range(len(centros_imagen)):
        if centros_imagen[c]==(0, 0):
            sum = sum + 1
    n = 0        
    while n<sum:
        centros_imagen.remove((0, 0))
        n = n+1
    for c in range(len(centros_imagen)):
        cv2.circle(normal, centros_imagen[c], 1, (255,255,255), -1)        
    centros_imagen.sort
    primer_punto = asi.esquina_sup_izq(centros_imagen)
    #print(primer_punto)
    lista_ordenada = list()
    lista_ordenada.append(primer_punto)
    modo_de_busqueda = 'hacia el lado'
    lista_ordenada = asi.asignar_orden_a_puntos(centros_imagen, primer_punto, lista_ordenada, modo_de_busqueda)
    print(lista_ordenada)   

    ruta_de_imagen = 'C:/Users/Peter/Desktop/PJ/prueba_opencv.png'
    print(ruta_de_imagen)
    return normal