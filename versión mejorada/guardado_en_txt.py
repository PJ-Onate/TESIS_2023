import time
import os
import asignacion as asi

def guardado(puntoA, puntoB, nombreA, nombreB):
    carpeta = r"C:\Users\Victor Rosales"
    archivo_txt = open(carpeta + r"\DISTANCIAS.txt", "a")
    distancia = asi.calculo_distancia(puntoA, puntoB)
    distancia = distancia*0.0518134715

    texto_punto_a = "Ubicacion " + nombreA +": " +str(puntoA) + "(" + str(time.ctime()) + ")"
    texto_punto_b = "Ubicacion " + nombreB + ": "+str(puntoB) + "(" + str(time.ctime()) + ")"
    texto_distancias = "Distancia entre " +nombreA + " y "+nombreB+ ": " + str(distancia) + " milimetros"
    archivo_txt.write (texto_punto_a)
    archivo_txt.write(os.linesep)
    archivo_txt.write (texto_punto_b)
    archivo_txt.write(os.linesep)
    archivo_txt.write(texto_distancias)
    archivo_txt.write(os.linesep)

    return (texto_punto_a, texto_punto_b, texto_distancias)
