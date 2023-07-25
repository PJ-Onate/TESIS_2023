import cv2

def lista_de_centros(contornos):
    lista = []
    for c in contornos:
        M = cv2.moments(c)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
        else:
            cX, cY = 0, 0     
        lista.append((cX, cY)) 
    return lista