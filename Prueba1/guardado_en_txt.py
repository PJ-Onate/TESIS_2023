import time
import os
import asignacion as asi

def guardado(puntoA, puntoB, nombreA, nombreB):
    carpeta = r"C:\Users\Peter\Desktop\PJ"
    archivo_txt = open(carpeta + r"\DISTANCIAS.txt", "a")
    distancia = asi.calculo_distancia(puntoA, puntoB)

    archivo_txt.write ("Ubicacion " + nombreA +": " +str(puntoA) + "(" + str(time.ctime()) + ")")
    archivo_txt.write(os.linesep)
    archivo_txt.write ("Ubicacion " + nombreB + ": "+str(puntoB) + "(" + str(time.ctime()) + ")")
    archivo_txt.write(os.linesep)
    archivo_txt.write("Distancia entre " +nombreA + " y "+nombreB+ ": " + str(distancia))
    archivo_txt.write(os.linesep)
