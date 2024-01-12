import tkinter as tk
from tkinter import ttk
from tkinter.constants import *
import oneCameraCapture
import PIL.Image, PIL.ImageTk
import cv2
import time
import numpy as np
import asignacion as asi
import guardado_en_txt as txt
from datetime import datetime, timedelta
from threading import Thread

tupla_esquinas = []


puntos_img_usuario = []
formato = ('%Y-%m-%d %H:%M:%S')



def posicion(event):
    global puntos_img_usuario
    global tupña_esquinas
    #print(tupla_esquinas[0])
    #print(event.x, event.y)
    print(puntos_img_usuario)
    #print("")
    #print("")
    print((event.x, event.y))
    print("hola")
    for elemento in puntos_img_usuario:
        if((event.x >= (elemento[0]-5)) & (event.x <= (elemento[0]+5))) & ((event.y >=(elemento[1]-5)) & (event.y <=(elemento[1]+5))):
            print(elemento)
    print("fin")
    print("")

class Page(tk.Frame):#clase Page, es una clase derivada (herencia), Page hereda atributos y funciones  de la clase tk.Frame
     

    def __init__(self, parent, window):#Se inicializa la clase

        tk.Frame.__init__(self, parent) #Se inicializa una insrancia de Frame
        self.window = window #se asigna valor al atributo window de la clase Page, ¿¿window ws un parámetro heredado??
        self.window.title = "Title" #el titulo de window es "Title"

        #Open camera source
        self.vid = oneCameraCapture.cameraCapture()#el atribu9to vid es el resultado de una función exeterna

        #Create a canvas that will fit the camera source
        self.ventana = tk.Frame(window, width=1000,height=600)
        self.ventana.grid(row=0, column=0)
        self.canvas = tk.Canvas(self.ventana, width=1000,height=600)
        self.canvas.grid(row=0, column=0)


        #menuFrame = ttk.Labelframe(window, text=("Menu"))
        #menuFrame.grid(row=1, column=0, sticky="NSW",
        #    padx=5, pady=2)
        

        #Button that lets the user take a snapshot

        self.muestreo_datos = tk.Listbox(window, width = 125, height = 40)
        self.muestreo_datos.grid(row=0, column=1, padx=10, pady=10)
        self.muestreo_datos.insert(0, "Muestreo de datos")


        self.formulario_inicio_exp = tk.Frame(window)
        tk.Label(self.formulario_inicio_exp, text = "Fecha inicio de experimento: ").grid(row=0, column=0)
        self.formulario_inicio_exp.grid(row=1, column=0)

        self.formulario_salto_exp = tk.Frame(window)
        tk.Label(self.formulario_salto_exp, text = "Lapso de captura de datos: ").grid(row=0, column=0)
        self.formulario_salto_exp.grid(row=2, column=0)

        self.formulario_fin_exp = tk.Frame(window)
        tk.Label(self.formulario_fin_exp, text = "Fecha fin de experimento:: ").grid(row=0, column=0)
        self.formulario_fin_exp.grid(row=3, column=0)

        self.btnSaveImage = tk.Button(window, text="Iniciar Experimento", command=self.start_threadhilo)
        self.btnSaveImage.grid(row=4, column=0)
        #tk.Label(self.formulario, text = "Capturar datos cada:").grid(row=0,column=0)

        #formuario inicio
        form_anio_inicio = tk.Frame(self.formulario_inicio_exp)
        form_anio_inicio.grid(row =1, column=0)
        tk.Label(form_anio_inicio, text="año").grid(row=0, column=0)
        self.entry_anio_inicio = tk.Entry(form_anio_inicio)
        self.entry_anio_inicio.insert(0, "0")
        self.entry_anio_inicio.grid(row=1, column=0)

        form_mes_inicio = tk.Frame(self.formulario_inicio_exp)
        form_mes_inicio.grid(row =1, column=1)
        tk.Label(form_mes_inicio, text="mes").grid(row=0, column=0)
        self.entry_mes_inicio = tk.Entry(form_mes_inicio)
        self.entry_mes_inicio.insert(0, "0")
        self.entry_mes_inicio.grid(row=1, column=0)


        form_dia_inicio = tk.Frame(self.formulario_inicio_exp)
        form_dia_inicio.grid(row =1, column=2)
        tk.Label(form_dia_inicio, text="día").grid(row=0, column=0)
        self.entry_dia_inicio = tk.Entry(form_dia_inicio)
        self.entry_dia_inicio.insert(0, "0")
        self.entry_dia_inicio.grid(row=1, column=0)

        form_hora_inicio = tk.Frame(self.formulario_inicio_exp)
        form_hora_inicio.grid(row =1, column=3)
        tk.Label(form_hora_inicio, text="hora").grid(row=0, column=0)
        self.entry_hora_inicio = tk.Entry(form_hora_inicio)
        self.entry_hora_inicio.insert(0, "00")
        self.entry_hora_inicio.grid(row=1, column=0)

        form_min_inicio = tk.Frame(self.formulario_inicio_exp)
        form_min_inicio.grid(row =1, column=4)
        tk.Label(form_min_inicio, text="minuto").grid(row=0, column=0)
        self.entry_min_inicio = tk.Entry(form_min_inicio)
        self.entry_min_inicio.insert(0, "00")
        self.entry_min_inicio.grid(row=1, column=0)

        form_seg_inicio = tk.Frame(self.formulario_inicio_exp)
        form_seg_inicio.grid(row =1, column=5)
        tk.Label(form_seg_inicio, text="segundo").grid(row=0, column=0)
        self.entry_seg_inicio = tk.Entry(form_seg_inicio)
        self.entry_seg_inicio.insert(0, "00")
        self.entry_seg_inicio.grid(row=1, column=0)

        form_mil_inicio = tk.Frame(self.formulario_inicio_exp)
        form_mil_inicio.grid(row =1, column=6)
        tk.Label(form_mil_inicio, text="milisegundo").grid(row=0, column=0)
        self.entry_mil_inicio = tk.Entry(form_mil_inicio)
        self.entry_mil_inicio.insert(0, "00")
        self.entry_mil_inicio.grid(row=1, column=0)        

        #formuario salto
        form_anio_salto = tk.Frame(self.formulario_salto_exp)
        form_anio_salto.grid(row =1, column=0)
        tk.Label(form_anio_salto, text="año").grid(row=0, column=0)
        self.entry_anio_salto = tk.Entry(form_anio_salto)
        self.entry_anio_salto.insert(0, "0")
        self.entry_anio_salto.grid(row=1, column=0)

        form_dia_salto = tk.Frame(self.formulario_salto_exp)
        form_dia_salto.grid(row =1, column=1)
        tk.Label(form_dia_salto, text="día").grid(row=0, column=0)
        self.entry_dia_salto = tk.Entry(form_dia_salto)
        self.entry_dia_salto.insert(0, "0")
        self.entry_dia_salto.grid(row=1, column=0)

        form_hora_salto = tk.Frame(self.formulario_salto_exp)
        form_hora_salto.grid(row =1, column=2)
        tk.Label(form_hora_salto, text="hora").grid(row=0, column=0)
        self.entry_hora_salto = tk.Entry(form_hora_salto)
        self.entry_hora_salto.insert(0, "0")
        self.entry_hora_salto.grid(row=1, column=0)

        form_min_salto = tk.Frame(self.formulario_salto_exp)
        form_min_salto.grid(row =1, column=3)
        tk.Label(form_min_salto, text="minuto").grid(row=0, column=0)
        self.entry_min_salto = tk.Entry(form_min_salto)
        self.entry_min_salto.insert(0, "0")
        self.entry_min_salto.grid(row=1, column=0)

        form_seg_salto = tk.Frame(self.formulario_salto_exp)
        form_seg_salto.grid(row =1, column=4)
        tk.Label(form_seg_salto, text="segundo").grid(row=0, column=0)
        self.entry_seg_salto = tk.Entry(form_seg_salto)
        self.entry_seg_salto.insert(0, "0")
        self.entry_seg_salto.grid(row=1, column=0)

        form_mil_salto = tk.Frame(self.formulario_salto_exp)
        form_mil_salto.grid(row =1, column=5)
        tk.Label(form_mil_salto, text="milisegundo").grid(row=0, column=0)
        self.entry_mil_salto = tk.Entry(form_mil_salto)
        self.entry_mil_salto.insert(0, "0")
        self.entry_mil_salto.grid(row=1, column=0)      


        #formuario fin
        form_anio_fin = tk.Frame(self.formulario_fin_exp)
        form_anio_fin.grid(row =1, column=0)
        tk.Label(form_anio_fin, text="año").grid(row=0, column=0)
        self.entry_anio_fin = tk.Entry(form_anio_fin)
        self.entry_anio_fin.insert(0, "0")
        self.entry_anio_fin.grid(row=1, column=0)

        form_mes_fin = tk.Frame(self.formulario_fin_exp)
        form_mes_fin.grid(row =1, column=1)
        tk.Label(form_mes_fin, text="mes").grid(row=0, column=0)
        self.entry_mes_fin = tk.Entry(form_mes_fin)
        self.entry_mes_fin.insert(0, "0")
        self.entry_mes_fin.grid(row=1, column=0)

        form_dia_fin = tk.Frame(self.formulario_fin_exp)
        form_dia_fin.grid(row =1, column=2)
        tk.Label(form_dia_fin, text="día").grid(row=0, column=0)
        self.entry_dia_fin = tk.Entry(form_dia_fin)
        self.entry_dia_fin.insert(0, "0")
        self.entry_dia_fin.grid(row=1, column=0)

        form_hora_fin = tk.Frame(self.formulario_fin_exp)
        form_hora_fin.grid(row =1, column=3)
        tk.Label(form_hora_fin, text="hora").grid(row=0, column=0)
        self.entry_hora_fin = tk.Entry(form_hora_fin)
        self.entry_hora_fin.insert(0, "00")
        self.entry_hora_fin.grid(row=1, column=0)

        form_min_fin = tk.Frame(self.formulario_fin_exp)
        form_min_fin.grid(row =1, column=4)
        tk.Label(form_min_fin, text="minuto").grid(row=0, column=0)
        self.entry_min_fin = tk.Entry(form_min_fin)
        self.entry_min_fin.insert(0, "00")
        self.entry_min_fin.grid(row=1, column=0)

        form_seg_fin = tk.Frame(self.formulario_fin_exp)
        form_seg_fin.grid(row =1, column=5)
        tk.Label(form_seg_fin, text="segundo").grid(row=0, column=0)
        self.entry_seg_fin = tk.Entry(form_seg_fin)
        self.entry_seg_fin.insert(0, "00")
        self.entry_seg_fin.grid(row=1, column=0)

        form_mil_fin = tk.Frame(self.formulario_fin_exp)
        form_mil_fin.grid(row =1, column=6)
        tk.Label(form_mil_fin, text="milisegundo").grid(row=0, column=0)
        self.entry_mil_fin = tk.Entry(form_mil_fin)
        self.entry_mil_fin.insert(0, "00")
        self.entry_mil_fin.grid(row=1, column=0)

        self.delay=100
        self.update()
        #self.window.mainloop()


   
    
    def command(self):
        global formato
        inicio = self.entry_anio_inicio.get() + '-'+self.entry_mes_inicio.get()+'-'+self.entry_dia_inicio.get()+' '+self.entry_hora_inicio.get()+':'+self.entry_min_inicio.get()+':'+self.entry_seg_inicio.get()    
        inicio = datetime.strptime(inicio, formato)

        fin = self.entry_anio_fin.get() + '-'+self.entry_mes_fin.get()+'-'+self.entry_dia_fin.get()+' '+self.entry_hora_fin.get()+':'+self.entry_min_fin.get()+':'+self.entry_seg_fin.get()  
        fin = datetime.strptime(fin, formato)
        lapso = inicio
        print("Inicio de experimento: " + str(inicio))
        self.muestreo_datos.insert(1, "Fecha de inicio: "+str(inicio))
        self.muestreo_datos.insert(2, "Fecha de fin: "+str(fin))
        while datetime.now() < fin:
            hora = datetime.now().replace(microsecond=0)    
            if hora == lapso:
                lapso = lapso + timedelta(days =int(self.entry_anio_salto.get())*365 +int(self.entry_dia_salto.get()), minutes=int(self.entry_min_salto.get()), seconds=int(self.entry_seg_salto.get()))
                print("La proxima captura es en: "+ str(lapso))
                 
                #asi.calculo_distancia(self.lista[0], self.lista[1])
                #asi.calculo_distancia(self.lista[11], self.lista[12])
                #texto1, texto2, texto3 = txt.guardado(self.lista[0], self.lista[1], "Punto A", "Punto B")
                #texto4, texto5, texto6 = txt.guardado(self.lista[11], self.lista[12], "Punto C", "Punto D")
                #self.muestreo_datos.insert(3, " ")
                #self.muestreo_datos.insert(4, texto1)
                #self.muestreo_datos.insert(5, texto2)
                #self.muestreo_datos.insert(6, texto3)
                #self.muestreo_datos.insert(7, " ")
                #self.muestreo_datos.insert(8, texto4)
                #self.muestreo_datos.insert(9, texto5)
                #self.muestreo_datos.insert(10, texto6)
                
        print("Fin del experimento")

    def start_threadhilo(self):
            thread = Thread(target = self.command)
            thread.setDaemon(1)
            #alive.set()
            thread.start()


    def update(self):
        #Get a frame from cameraCapture
        global tupla_esquinas
        global puntos_img_usuario
        tupla_esquinas =[]
        puntos_img_usuario = []
        frame = self.vid.getFrame() #This is an array
        #https://stackoverflow.com/questions/48121916/numpy-resize-rescale-image/48121996
        #ret, frame = cv2.threshold(frame, 120, 255, 0)

        frame_gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        median = cv2.medianBlur(frame_gris, 15)
        gauss = cv2.GaussianBlur(median, (5, 5), 0)

        
        detector = cv2.FastFeatureDetector_create()
        keypoints = detector.detect(gauss, None)

        for keypoint in keypoints:
            radius = int(0.15 * keypoint.size)
            x, y = np.int64(keypoint.pt)
            cv2.circle(frame, (x, y), 15, 255, -1)
    
    #image = imutils.resize(dst, width = 600, height = 250)
 
            

        #cv2.circle(frame, tupla_esquinas[0][0], 15, 255, -1)
        #list = []
        #primer_punto = asi.esquina_sup_izq(tupla_esquinas)
        #list.append(primer_punto)
        #self.lista = asi.asignar_orden_a_puntos(tupla_esquinas, primer_punto, list, 'hacia el lado')

        #for tupla in lista:
        #    cv2.circle(frame, tupla, 15, 255, -1)

        

        #cv2.circle(frame, self.lista[0], 15, 255, -1)
        #cv2.circle(frame, self.lista[1], 15, 255, -1)

        #cv2.circle(frame, self.lista[11], 15, 255, -1)
        #cv2.circle(frame, self.lista[12], 15, 255, -1)


        frame = cv2.resize(frame, dsize=(1000, 600), interpolation=cv2.INTER_CUBIC)
        #OpenCV bindings for Python store an image in a NumPy array
        #Tkinter stores and displays images using the PhotoImage class
        # Use PIL (Pillow) to convert the NumPy ndarray to a PhotoImage
        self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
        self.canvas.create_image(500,300,image=self.photo)
        #self.canvas2.create_image(500,300,image=self.photo)


        self.window.after(self.delay, self.update)

    def actualizar(self):
        #Get a frame from cameraCapture
        global tupla_esquinas
        tupla_esquinas =[]
        frame = self.vid.getFrame() #This is an array
        #https://stackoverflow.com/questions/48121916/numpy-resize-rescale-image/48121996
        #ret, frame = cv2.threshold(frame, 120, 255, 0)

        frame = cv2.resize(frame, dsize=(1000, 600), interpolation=cv2.INTER_CUBIC)

        #OpenCV bindings for Python store an image in a NumPy array
        #Tkinter stores and displays images using the PhotoImage class
        # Use PIL (Pillow) to convert the NumPy ndarray to a PhotoImage
        self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
        self.canvas2.create_image(500,300,image=self.photo)
        #self.canvas2.create_image(500,300,image=self.photo)


        self.window.after(self.delay, self.actualizar)

    def saveImage(self):
        # Get a frame from the video source
        print(self.entry_anio.get())
        print(self.entry_dia.get())
        print(self.entry_hora.get())
        print(self.entry_min.get())
        print(self.entry_mil.get())    

        #cv2.imwrite("frame-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".jpg",
         #           cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))







