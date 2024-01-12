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
from tkinter import messagebox as MessageBox



copia = None
frame_gris = None

inicio = 1
asignacion = None
lista_de_pares = []


detener_camara = True

entry_id_interseccion = None
entry_id_punto_a = None
entry_id_punto_b = None

corners = []




formato = ('%Y-%m-%d %H:%M:%S')

lista_2=[]


img = None




def imprimir():
    global img
    cv2.imshow("img", img)
    cv2.waitKey(5) 
  
    # closing all open windows 
    cv2.destroyAllWindows() 


def hilo2():
    thread = Thread(target = imprimir)
    thread.setDaemon(1)
    #alive.set()
    thread.start()




i=0    
def prueba():
    lista_flujo_optico = []
    global lista_de_pares
    global copia
    global formato
    global entry_anio_inicio
    global entry_mes_inicio
    global entry_dia_inicio
    global entry_hora_inicio
    global entry_min_inicio
    global entry_seg_inicio

    global entry_anio_fin
    global entry_mes_fin
    global entry_dia_fin
    global entry_hora_fin
    global entry_min_fin
    global entry_seg_fin

    global vid

    global corners

    global img
    
    mask = np.zeros_like(copia)


    lk_params = dict( winSize = (15, 15), 
                      maxLevel = 2, 
                      criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 
                                  10, 0.03)) 
    
    global lista_2
    for par in lista_de_pares:
        lista_flujo_optico.append([par[3], par[4]])
        lista_2.append(par[3])
        lista_2.append(par[4])
    print(lista_2)

        
    for inter in lista_flujo_optico:
        #print(inter[0])
        cv2.circle(copia, inter[0], 5, (255, 255, 0), 15)
        #print(inter[1])
        cv2.circle(copia, inter[1], 5, (0, 255, 0), 15)


    
    old_gray =  cv2.cvtColor(copia, cv2.COLOR_BGR2GRAY)


    height, width = old_gray.shape
    print("priemra imagen: ", height, width)

    array_corners = np.array(corners)

    # Aplica la operación reshape
    array_corners = array_corners.reshape(-1, 1, 2)



    inicio = entry_anio_inicio.get() + '-'+entry_mes_inicio.get()+'-'+entry_dia_inicio.get()+' '+entry_hora_inicio.get()+':'+entry_min_inicio.get()+':'+entry_seg_inicio.get()    
    inicio = datetime.strptime(inicio, formato)

    fin = entry_anio_fin.get() + '-'+entry_mes_fin.get()+'-'+entry_dia_fin.get()+' '+entry_hora_fin.get()+':'+entry_min_fin.get()+':'+entry_seg_fin.get()  
    fin = datetime.strptime(fin, formato)
    lapso = inicio
    print("Inicio de experimento: " + str(inicio))
    while datetime.now() < fin:
        hora = datetime.now().replace(microsecond=0)    
        if hora == lapso:
            lapso = lapso + timedelta(days =int(entry_anio_salto.get())*365 +int(entry_dia_salto.get()), minutes=int(entry_min_salto.get()), seconds=int(entry_seg_salto.get()))
            print("La proxima captura es en: "+ str(lapso))

            #cap = oneCameraCapture.cameraCapture()
            frame = vid.getFrame() #This is an array
            #https://stackoverflow.com/questions/48121916/numpy-resize-rescale-image/48121996
            #ret, frame = cv2.threshold(frame, 120, 255, 0)

            frame_gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            height, width = frame_gris.shape
            print("segunda imagen: ", height, width)
            #median = cv2.medianBlur(frame_gris, 15)
            #frame_gris = cv2.GaussianBlur(median, (5, 5), 0)
            p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, 
                                               frame_gris, 
                                               array_corners, None, 
                                               **lk_params)
            good_new = None
            if p1 is not None:
                good_new = p1[st == 1]
                good_old = array_corners[st == 1]     

                for i, (new, old) in enumerate(zip(good_new, good_old)): 
                    a, b = new.ravel() 
                    c, d = old.ravel() 

                    mask = cv2.line(mask, (int(a), int(b)), (int(c), int(d)), (0, 255, 0), 2) 
                    frame = cv2.circle(frame, (int(a), int(b)), 5, (0, 255, 0), 9)

         
            for corner in corners:     
                a,b = corner.ravel()
                a = int(a)
                b = int(b)
            #   cv2.circle(frame, (a,b), 15, 255, -1)
                #tupla_esquinas.append([(a,b), (int(a*0.408496), int(b*0.292968))])
                #puntos_img_usuario.append((int(a*0.408496), int(b*0.292968)))
                #print(puntos_img_usuario[0])
         #       self.canvas.bind("<Button-1>", posicion)

            #for i, (new, old) in enumerate(zip(good_new, good_old)): 
            #    a, b = new.ravel() 
            #    c, d = old.ravel() 

            #    mask = cv2.line(mask, (int(a), int(b)), (int(c), int(d)), (0, 255, 0), 2) 
            #    frame = cv2.circle(frame, (int(a), int(b)), 5, (0, 255, 0), -1)
            #    self.canvas.bind("<Button-1>", posicion)

            global img
            img = cv2.add(frame, mask) 
                 
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

            img = cv2.resize(img, dsize=(1000, 600), interpolation=cv2.INTER_CUBIC)
            cv2.imwrite("C:/Users/Victor Rosales/Desktop/TESIS/TESIS_2023/Analizador de imágenes/Prueba1/img"+str(i)+".jpg", img)
            #hilo2()
            #cv2.imshow("imagen", img)
















def guardado():
    global inicio
    global asignacion
    global lista_de_pares

    global punto_a
    global punto_b

    global entry_id_interseccion
    global entry_id_punto_a
    global entry_id_punto_b

    var = False
    for par in lista_de_pares:
        print(par[0], entry_id_interseccion.get())
        if par[0]== entry_id_interseccion.get() or par[1] == entry_id_punto_a.get() or par[2] == entry_id_punto_b.get():
            MessageBox.showinfo("Error", "Una de las IDs ya está ingresada, reingrese: ") # título, mensaje
            var = True

    if var == False:           
        lista_de_pares.append([entry_id_interseccion.get(), entry_id_punto_a.get(), entry_id_punto_b.get(), punto_a, punto_b])
        inicio = 1
        asignacion.destroy()

    print(lista_de_pares)



punto_a = None
punto_b = None
def posicion(event):
    global puntos_img_usuario
    global tupla_esquinas
    global trans
    global inicio
    global asignacion

    global entry_id_interseccion
    global entry_id_punto_a
    global entry_id_punto_b
    global punto_a
    global punto_b


    global detener_camara

    for elemento in puntos_img_usuario:
        if((event.x >= (elemento[0]-5)) & (event.x <= (elemento[0]+5))) & ((event.y >=(elemento[1]-5)) & (event.y <=(elemento[1]+5))):
            detener_camara = False
            if inicio == 1:
                print(elemento)
                for tupla in tupla_esquinas:
                    if tupla[1] == elemento:
                        elemento = tupla[0]
                        print(tupla)
                        break
                    
                print(elemento)
                punto_a = elemento
                asignacion = tk.Toplevel(trans)
                asignacion.title("ID de intersecciones")
                
                tk.Label(asignacion, text="Ingrese ID para el par de intersecciones: ").grid(row=0, column=0)
                entry_id_interseccion = tk.Entry(asignacion)
                entry_id_interseccion.grid(row=1, column=0)

                tk.Label(asignacion, text="Ingrese ID Punto A: ").grid(row=2, column=0)
                entry_id_punto_a = tk.Entry(asignacion)
                entry_id_punto_a.grid(row=3, column=0)

                inicio = inicio + 1
                asignacion.transient(master=root)
                
    
            else:
                if  inicio == 2:
                    print(elemento)
                    for tupla in tupla_esquinas:
                        if tupla[1] == elemento:
                            elemento = tupla[0]
                            print(tupla)
                            break
                    punto_b = elemento
                    print(elemento)
                    tk.Label(asignacion, text="Ingrese ID Punto B: ").grid(row=4, column=0)
                    entry_id_punto_b = tk.Entry(asignacion)
                    entry_id_punto_b.grid(row=5, column=0)

                    guardar_int = tk.Button(asignacion, text = "Guardar intersección",  command = guardado)
                    guardar_int.grid(row = 6, column=0)




def start_threadhilo():
    thread = Thread(target = prueba)
    thread.setDaemon(1)
    #alive.set()
    thread.start()
vid = None
class Page(tk.Frame):#clase Page, es una clase derivada (herencia), Page hereda atributos y funciones  de la clase tk.Frame
     

    def __init__(self, parent, window):#Se inicializa la clase

        tk.Frame.__init__(self, parent) #Se inicializa una insrancia de Frame
        self.window = window #se asigna valor al atributo window de la clase Page, ¿¿window ws un parámetro heredado??
        #self.window.title = "Title" #el titulo de window es "Title"

        #Open camera source
        global vid
        vid = oneCameraCapture.cameraCapture()#el atribu9to vid es el resultado de una función exeterna

        #Create a canvas that will fit the camera source

        self.titulo = tk.Label(window, text = "Intersecciones encontradas", font=("New Times Roman", 20))
        self.titulo.grid(row=0, column=0)
        self.ventana = tk.Frame(window, width=1000,height=600)
        self.ventana.grid(row=1, column=0)
        self.canvas = tk.Canvas(self.ventana, width=1000,height=600)
        self.canvas.grid(row=0, column=0, pady = (50,50))


        #menuFrame = ttk.Labelframe(window, text=("Menu"))
        #menuFrame.grid(row=1, column=0, sticky="NSW",
        #    padx=5, pady=2)
        

        #Button that lets the user take a snapshot

        self.muestreo_datos = tk.Listbox(window, width = 50, height = 40)
        self.muestreo_datos.grid(row=1, column=1, padx=10, pady= (30,0))
        self.muestreo_datos.insert(0, "Intersecciones elegidas")

        self.inicio_experimento = tk.Button(window, text = "Iniciar experimento", command =start_threadhilo)

        self.inicio_experimento.grid(row = 2, column=0)


        self.delay=100

        
        self.update()
        #self.window.mainloop()


   
    
    def command(self):
        global formato
        global frame_gris
        global frame
        
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





    def update(self):
        #Get a frame from cameraCapture
        global tupla_esquinas
        global puntos_img_usuario
        global detener_camara
        global frame_gris
        global copia
        global vid
        global corners

        if detener_camara == True:
            tupla_esquinas =[]
            puntos_img_usuario = []
            frame = vid.getFrame() #This is an array
            
            copia = vid.getFrame()
            #https://stackoverflow.com/questions/48121916/numpy-resize-rescale-image/48121996
            #ret, frame = cv2.threshold(frame, 120, 255, 0)

            frame_gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            median = cv2.medianBlur(frame_gris, 15)
            gauss = cv2.GaussianBlur(median, (5, 5), 0)
            dst = cv2.cornerHarris(gauss,64,31,0.21)
            dst = cv2.dilate(dst,None)
            
       
            ret, dst = cv2.threshold(dst,0.01*dst.max(),255,0)
            dst = np.uint8(dst)
        
            ret, labels, stats, centroids = cv2.connectedComponentsWithStats(dst)
            criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 0.3)
            corners = cv2.cornerSubPix(gauss,np.float32(centroids),(5,5),(-1,-1),criteria)
     
            for corner in corners:     
                a,b = corner.ravel()
                a = int(a)
                b = int(b)
           
                cv2.circle(frame, (a,b), 15, 255, -1)
                tupla_esquinas.append([(a,b), (int(a*0.408496), int(b*0.292968))])
                puntos_img_usuario.append((int(a*0.408496), int(b*0.292968)))
              
                self.canvas.bind("<Button-1>", posicion)
            #FIN    
            
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




def hilo():
    global entry_anio_inicio
    global entry_mes_inicio
    global entry_dia_inicio
    global entry_hora_inicio
    global entry_min_inicio
    global entry_seg_inicio

    global entry_anio_fin
    global entry_mes_fin
    global entry_dia_fin
    global entry_hora_fin
    global entry_min_fin
    global entry_seg_fin
    
    
    inicio = entry_anio_inicio.get() + '-'+entry_mes_inicio.get()+'-'+entry_dia_inicio.get()+' '+entry_hora_inicio.get()+':'+entry_min_inicio.get()+':'+entry_seg_inicio.get()    
    inicio = datetime.strptime(inicio, formato)

    fin = entry_anio_fin.get() + '-'+entry_mes_fin.get()+'-'+entry_dia_fin.get()+' '+entry_hora_fin.get()+':'+entry_min_fin.get()+':'+entry_seg_fin.get()  
    fin = datetime.strptime(fin, formato)

    if inicio>fin:
        MessageBox.showinfo("Error", "La fecha de inicio es una fecha posterior a la fecha de fin. Reingrese una fecha válida") # título, mensaje

    else: 
        thread = Thread(target = transmision)
        thread.setDaemon(1)
        thread.start()


trans = None
def transmision():
    global root
    global trans
    trans = tk.Toplevel(root)
    trans.title("Elección de esquinas")
    testWidget = Page(trans, trans)
    testWidget.grid(row=0, column=1, sticky="W")
    


tupla_esquinas = []


puntos_img_usuario = []
formato = ('%Y-%m-%d %H:%M:%S')

root = tk.Tk()
root.title("Menú")
#root.state('zoomed')

#frame de formulario
formulario = tk.Frame(root)
formulario.grid(row=0, column=0)


#label "Iniciar experimento"
form_titulo = tk.Label(formulario, text="Iniciar experimento", font=("New Times Roman", 20))
form_titulo.grid(row=0, column=0)


#nombre de experimento
form_nombre_exp = tk.Frame(formulario)
tk.Label(form_nombre_exp, text = "Nombre del experimento").grid(row=0, column=0)
form_nombre_exp.grid(row=1, column=0)
entry_exp = tk.Entry(form_nombre_exp)
entry_exp.grid(row=1, column=0)


#nombre de encargado del experimento
form_encargado = tk.Frame(formulario)
tk.Label(form_encargado, text = "Nombre del encargado del experimento").grid(row=0, column=0)
form_encargado.grid(row=2, column=0)
entry_encargado = tk.Entry(form_encargado)
entry_encargado.grid(row=1, column=0)

#Descripción
form_descripcion = tk.Frame(formulario)
tk.Label(form_descripcion, text = "Descripción (opcional)").grid(row=0, column=0)
form_descripcion.grid(row=3, column=0)
entry_descripcion = tk.Entry(form_descripcion)
entry_descripcion.grid(row=1, column=0)


frame_inicio_exp = tk.Frame(formulario)
tk.Label(frame_inicio_exp, text = "Fecha inicio de experimento: ").grid(row=0, column=0)
frame_inicio_exp.grid(row=4, column=0)

frame_salto_exp = tk.Frame(formulario)
tk.Label(frame_salto_exp, text = "Lapso de captura de datos: ").grid(row=0, column=0)
frame_salto_exp.grid(row=5, column=0)

frame_fin_exp = tk.Frame(formulario)
tk.Label(frame_fin_exp, text = "Fecha fin de experimento:: ").grid(row=0, column=0)
frame_fin_exp.grid(row=6, column=0)

btnSaveImage = tk.Button(formulario, text="Escoger interseccioness", command = hilo)
btnSaveImage.grid(row=7, column=0)


#formulario inicio
form_anio_inicio = tk.Frame(frame_inicio_exp)
form_anio_inicio.grid(row =1, column=0)
tk.Label(form_anio_inicio, text="año").grid(row=0, column=0)
entry_anio_inicio = tk.Entry(form_anio_inicio)
entry_anio_inicio.insert(0, "0")
entry_anio_inicio.grid(row=1, column=0)

form_mes_inicio = tk.Frame(frame_inicio_exp)
form_mes_inicio.grid(row =1, column=1)
tk.Label(form_mes_inicio, text="mes").grid(row=0, column=0)
entry_mes_inicio = tk.Entry(form_mes_inicio)
entry_mes_inicio.insert(0, "0")
entry_mes_inicio.grid(row=1, column=0)


form_dia_inicio = tk.Frame(frame_inicio_exp)
form_dia_inicio.grid(row =1, column=2)
tk.Label(form_dia_inicio, text="día").grid(row=0, column=0)
entry_dia_inicio = tk.Entry(form_dia_inicio)
entry_dia_inicio.insert(0, "0")
entry_dia_inicio.grid(row=1, column=0)

form_hora_inicio = tk.Frame(frame_inicio_exp)
form_hora_inicio.grid(row =1, column=3)
tk.Label(form_hora_inicio, text="hora").grid(row=0, column=0)
entry_hora_inicio = tk.Entry(form_hora_inicio)
entry_hora_inicio.insert(0, "00")
entry_hora_inicio.grid(row=1, column=0)

form_min_inicio = tk.Frame(frame_inicio_exp)
form_min_inicio.grid(row =1, column=4)
tk.Label(form_min_inicio, text="minuto").grid(row=0, column=0)
entry_min_inicio = tk.Entry(form_min_inicio)
entry_min_inicio.insert(0, "00")
entry_min_inicio.grid(row=1, column=0)

form_seg_inicio = tk.Frame(frame_inicio_exp)
form_seg_inicio.grid(row =1, column=5)
tk.Label(form_seg_inicio, text="segundo").grid(row=0, column=0)
entry_seg_inicio = tk.Entry(form_seg_inicio)
entry_seg_inicio.insert(0, "00")
entry_seg_inicio.grid(row=1, column=0)      

#formulario salto
form_anio_salto = tk.Frame(frame_salto_exp)
form_anio_salto.grid(row =1, column=0)
tk.Label(form_anio_salto, text="año").grid(row=0, column=0)
entry_anio_salto = tk.Entry(form_anio_salto)
entry_anio_salto.insert(0, "0")
entry_anio_salto.grid(row=1, column=0)

form_mes_salto = tk.Frame(frame_salto_exp)
form_mes_salto.grid(row =1, column=1)
tk.Label(form_mes_salto, text="mes").grid(row=0, column=0)
entry_mes_salto = tk.Entry(form_mes_salto)
entry_mes_salto.insert(0, "0")
entry_mes_salto.grid(row=1, column=0)

form_dia_salto = tk.Frame(frame_salto_exp)
form_dia_salto.grid(row =1, column=2)
tk.Label(form_dia_salto, text="día").grid(row=0, column=0)
entry_dia_salto = tk.Entry(form_dia_salto)
entry_dia_salto.insert(0, "0")
entry_dia_salto.grid(row=1, column=0)

form_hora_salto = tk.Frame(frame_salto_exp)
form_hora_salto.grid(row =1, column=3)
tk.Label(form_hora_salto, text="hora").grid(row=0, column=0)
entry_hora_salto = tk.Entry(form_hora_salto)
entry_hora_salto.insert(0, "0")
entry_hora_salto.grid(row=1, column=0)

form_min_salto = tk.Frame(frame_salto_exp)
form_min_salto.grid(row =1, column=4)
tk.Label(form_min_salto, text="minuto").grid(row=0, column=0)
entry_min_salto = tk.Entry(form_min_salto)
entry_min_salto.insert(0, "0")
entry_min_salto.grid(row=1, column=0)

form_seg_salto = tk.Frame(frame_salto_exp)
form_seg_salto.grid(row =1, column=5)
tk.Label(form_seg_salto, text="segundo").grid(row=0, column=0)
entry_seg_salto = tk.Entry(form_seg_salto)
entry_seg_salto.insert(0, "0")
entry_seg_salto.grid(row=1, column=0)

#formulario fin
form_anio_fin = tk.Frame(frame_fin_exp)
form_anio_fin.grid(row =1, column=0)
tk.Label(form_anio_fin, text="año").grid(row=0, column=0)
entry_anio_fin = tk.Entry(form_anio_fin)
entry_anio_fin.insert(0, "0")
entry_anio_fin.grid(row=1, column=0)

form_mes_fin = tk.Frame(frame_fin_exp)
form_mes_fin.grid(row =1, column=1)
tk.Label(form_mes_fin, text="mes").grid(row=0, column=0)
entry_mes_fin = tk.Entry(form_mes_fin)
entry_mes_fin.insert(0, "0")
entry_mes_fin.grid(row=1, column=0)

form_dia_fin = tk.Frame(frame_fin_exp)
form_dia_fin.grid(row =1, column=2)
tk.Label(form_dia_fin, text="día").grid(row=0, column=0)
entry_dia_fin = tk.Entry(form_dia_fin)
entry_dia_fin.insert(0, "0")
entry_dia_fin.grid(row=1, column=0)

form_hora_fin = tk.Frame(frame_fin_exp)
form_hora_fin.grid(row =1, column=3)
tk.Label(form_hora_fin, text="hora").grid(row=0, column=0)
entry_hora_fin = tk.Entry(form_hora_fin)
entry_hora_fin.insert(0, "00")
entry_hora_fin.grid(row=1, column=0)

form_min_fin = tk.Frame(frame_fin_exp)
form_min_fin.grid(row =1, column=4)
tk.Label(form_min_fin, text="minuto").grid(row=0, column=0)
entry_min_fin = tk.Entry(form_min_fin)
entry_min_fin.insert(0, "00")
entry_min_fin.grid(row=1, column=0)

form_seg_fin = tk.Frame(frame_fin_exp)
form_seg_fin.grid(row =1, column=5)
tk.Label(form_seg_fin, text="segundo").grid(row=0, column=0)
entry_seg_fin = tk.Entry(form_seg_fin)
entry_seg_fin.insert(0, "00")
entry_seg_fin.grid(row=1, column=0)


#formulario de historial
historial = tk.Frame(root)
historial.grid(row=0, column=1)
tk.Label(historial, text = "Historial",  font=("New Times Roman", 20)).grid(row=0, column=0, padx=(100,100))

lista_de_exps = tk.Listbox(historial)
lista_de_exps.grid(row = 1, column=0, padx=(100,100))









#stestWidget = Page(root, root) #una instancia de la clase Page, con parámetros root, la ventana que se acaba de crear.Page hereda elementos de un widget Frane, y se lemañaden algunos elementos más en la  definición de clase
#testWidget.grid(row=0, column=1, sticky="W")
#btn = Button(root, text="Elegir imagen", width=25, command=elegir_imagen)
#btn.grid(column=0, row=0, padx=5, pady=5) 

root.mainloop()




