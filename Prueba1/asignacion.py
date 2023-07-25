from math import sqrt

def calculo_distancia(x,y):
    distancia_enre_puntos = sqrt(((x[0]-y[0])**2)+((x[1]-y[1])**2))
    return distancia_enre_puntos

def esquina_sup_izq(puntos_encontrados):
    for c in range(len(puntos_encontrados)):
        distancia_a_la_esquina = calculo_distancia(puntos_encontrados[c],(0,0))
        if c == 0:
            esquina = puntos_encontrados[c]
            distancia_mas_proxima = distancia_a_la_esquina
        else:
            if distancia_a_la_esquina < distancia_mas_proxima:
                distancia_mas_proxima = distancia_a_la_esquina
                esquina = puntos_encontrados[c]      
    return(esquina)

def asignar_orden_a_puntos(puntos_encontrados, primer_punto, lista_ordenada, modo_de_busqueda):    
    #primer_punto = esquina_sup_izq(puntos_encontrados)
    #lista_ordenada = list()
    terminar = False
    sumatoria = 1  
    while terminar == False:
        #print(primer_punto)
        lista_del_punto_mas_cercano_al_menos = list()
        for c in range(len(puntos_encontrados)):
            lista_del_punto_mas_cercano_al_menos.append(puntos_encontrados[c])
            if len(lista_del_punto_mas_cercano_al_menos)>1:
                for j in range(len(lista_del_punto_mas_cercano_al_menos)-1, -1, -1):
                    if calculo_distancia(lista_del_punto_mas_cercano_al_menos[j], primer_punto) > calculo_distancia(puntos_encontrados[c], primer_punto):
                        variable = lista_del_punto_mas_cercano_al_menos[j]
                        lista_del_punto_mas_cercano_al_menos[j+1] = variable
                        lista_del_punto_mas_cercano_al_menos[j] = puntos_encontrados[c]  
               
        for c in range(len(lista_del_punto_mas_cercano_al_menos)):
            if lista_del_punto_mas_cercano_al_menos[c] != primer_punto:
                if modo_de_busqueda == 'hacia el lado':
                    if primer_punto[0] < lista_del_punto_mas_cercano_al_menos[c][0]:
                        tangente = (calculo_distancia((lista_del_punto_mas_cercano_al_menos[c][0],primer_punto[1]),lista_del_punto_mas_cercano_al_menos[c]))/(calculo_distancia((lista_del_punto_mas_cercano_al_menos[c][0],primer_punto[1]),primer_punto))
                        if (tangente < 0.08) & (tangente >-0.08):
                            primer_punto = lista_del_punto_mas_cercano_al_menos[c]
                            lista_ordenada.append(primer_punto)
                            sumatoria = sumatoria+1
                            #print(sumatoria)
                            break
                else:        
                    if modo_de_busqueda == 'hacia abajo':            
                        if primer_punto[1]< lista_del_punto_mas_cercano_al_menos[c][1]:
                            seno = (calculo_distancia((lista_del_punto_mas_cercano_al_menos[c][0],primer_punto[1]),lista_del_punto_mas_cercano_al_menos[c]))/(calculo_distancia((lista_del_punto_mas_cercano_al_menos[c]),primer_punto))
                            if(seno < 1)&(seno>0.98):
                                primer_punto = lista_del_punto_mas_cercano_al_menos[c]
                                lista_ordenada.append(primer_punto)
                                modo_de_busqueda = 'hacia el lado'
                                break
                        if(c+1) == len(lista_del_punto_mas_cercano_al_menos):
                            terminar = True                     

        if (c+1)==len(lista_del_punto_mas_cercano_al_menos):
            primer_punto = lista_ordenada[len(lista_ordenada)-sumatoria]
            modo_de_busqueda = 'hacia abajo' 
            sumatoria = 1         
    return lista_ordenada

                    
