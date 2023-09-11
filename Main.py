
import pytesseract
import re
from PIL import Image
import cv2
import numpy as np
from fuzzywuzzy import fuzz
import pyautogui
import keyboard
from datetime import datetime
import os 

from Moduls.Almacena_Imagenes import Ejecutor
from Moduls.Guardar_Datos import Almacenamiento_Definitivo
from Moduls.Tiempo_peloton import Determinar_Errores






################################################     DATOSD MOPDIFICABLES


Nombres=["[Vpr]-Sicario","cheliRp","garnacho","Kaleroth"]       #Cambiar Nombres en la lista    ["[Vpr]-Sicario","cheliRp","Kaleroth"]
 

lenguaje='spa' #   'eng'     'spa'



####-------------------------------------------------------------------------------------   Datos Fijos








if lenguaje == 'spa':
    daño_infli=["Daños infligidos"]                             # ------------------------------   Modificar despues
    supervi=['tiempo de Supervivencia']
else:

    print("")
    daño_infli=['Damage Dealt']
    supervi=['Survival Time']           #-- ESTO AL USARLO EN INGLES PUEDE CAMBIAR LA DETECCION

Eliminaciones_Asistencias=['Elimin./Asistencias / K.O.']                                 
similitud_minima = 65
simillitud_Megaminima = 45


#############################################################   FUNCIONES ##############################################
def extraer_numeros(cadena):

    patron = r"[-+]?\d*\.\d+|\d+"
    numeros = re.findall(patron, cadena)
    
   
    numeros = [int(numero) for numero in numeros]
    
    return numeros


def extraer_dañoss(cadena):
    
    patron = r"[-+]?\d*\.\d+|\d+"
    numeros = re.findall(patron, cadena)
    
    if len(numeros)==2:
        numeros=numeros[0]+":" +numeros[1]
    

    
    return numeros


######################################        TOMA DE VALORES    ######################################################## 





print("Arranco")


       
ruta, Ruta_Para_enviar_imagenes=Ejecutor.Crea_Guarda()     # Toma de imagenes para el codigo

img = cv2.imread(R"{}".format(ruta))

img = np.array(img)

# Convertir numpy array a imagen OpenCV
img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
###################################################  EXPERIMENTOS      ##################

Vaolres_Guardados={}  







##################################################################"""
Tiempo_DE_Reaparicion=0
numbers=[]
#########        EMPIEZA RECORTES DE IMAGEN
''
height, width = img.shape[:2]
Superior=img[:height//3, :]

img = img[height//4:, :]
# Dividir la imagen en tres secciones verticales iguales
seccion1 = img[:, 0:width//3]
seccion2 = img[:, width//3:2*width//3]
seccion3 = img[:, 2*width//3:]

seccionSuperior=Superior[:, 2*width//3:]



#######################Recorte de la 1
height, width, _ = seccion1.shape
sección1_superior = seccion1[10: int(height*3), 0:width]  #    ANTES ESTABA ASI             seccion1[0: int(height*3), 0:width] 
sección1_superior_masrecortada = sección1_superior[:, 0:width//5*3]


#######################Recorte de la 2
height, width, _ = seccion2.shape
sección2_superior = seccion2[0: int(height*3), 0:width]  #seccion2[0:height//1, 0:width] #
sección2_superior_masrecortada = sección2_superior[:, 0:width//5*2]


################################################Recorte de la 3

height, width, _ = seccion3.shape
sección3_superior = seccion3[0: int(height*3), 0:width]  #seccion2[0:height//1, 0:width] #
sección3_superior_masrecortada = sección3_superior[:, 0:width//7*3]


#######################De l 3 saco los fragmentos
height, width, _ = sección3_superior_masrecortada.shape
AsistenciasSolo_dela3=sección3_superior_masrecortada[166:int(height/1*3), 0:width//6*3]


#########################################      TERMINAN RECORTES




height, width, _ = seccionSuperior.shape


sección3_superior_top = seccionSuperior[20:int(height*3)-10, 0:width]
sección3_superior_masrecortada_top = sección3_superior_top[125:int(height/1.7)-10, 240:width//7*3]



#####                                       MOSTRAR LOS RECORTES ELEGIDOS  ANTES DE SEGUIR CON EL CODIGO
#cv2.imshow("Sección 1 MAS RECORTADA", sección1_superior_masrecortada)
#cv2.imshow("Sección 2", sección1_superior)
#cv2.imshow("Sección 3", sección3_superior_masrecortada)
#cv2.imshow("Sección 2", sección2_superior_masrecortada)
#cv2.imshow("Sección 4", sección3_superior_masrecortada_top)
cv2.waitKey(0)
cv2.destroyAllWindows()


Secciones=[sección1_superior_masrecortada,sección2_superior_masrecortada,sección3_superior_masrecortada]
Tiempo_DE_Reaparicion='error en toma de'
numbers=[]
contador=0
Muertes_Asistencias=[]
##################################################################     IDENTIFICACION DE VALORES EN LA IMAGEN
for i in Secciones:

    text = pytesseract.image_to_string(i, lang=lenguaje)   # --------------  'spa'   'eng'  -------------------------------------------------    ESTA EN ESPAÑOL    
  
    
    text_list = text.split('\n')
    print(text_list)
    numbers=[]

   
    

   
    ##########################   Numeros

    ###--------------------------------------------------------------------------------------------      ELIMINACIONES ASISTENCIAS Y KO
  #  b=False
    for elem in text_list:   
     if '/' in elem:

       
        try:
            lista_vacia=extraer_numeros(elem)
        except:
          lista_vacia=[]

            
        if len(lista_vacia) == 3:
                Muertes_Asistencias = "/".join(str(x) for x in lista_vacia)
                break

          
  ## ###### -------------------------------------------------------------------------------------------         DAÑO REALIZADO         

    b=False                                        
    for i in text_list:
        similitud = fuzz.token_sort_ratio(daño_infli, i)
       
        Se_Paso = fuzz.token_sort_ratio(supervi, i)                                            
        


        if b==True:
           
           if Se_Paso >= similitud_minima:
              break
           
           numbers=extraer_numeros(i)

           if numbers!= []:
              break
           
           #numbers = [int(s) for s in text_list if s.isdigit()]

        if similitud >= similitud_minima:
            b=True
            
        

    ###############################
    
    



    Tiempo_DE_Reaparicion= 'Error en la toma de valores'

 ###-------------------------------------------------------------------------------------------------------------------------  TIEMPO DE  SUPERVIVENCIA
    for Tiempo_Reap in text_list:                              
       if ":" in  Tiempo_Reap:
          
         try:
          Tiempo_DE_Reaparicion=extraer_dañoss(Tiempo_Reap)     
         except:
          Tiempo_DE_Reaparicion=[]
        
            
         
         if (len(Tiempo_DE_Reaparicion))>5 or  Tiempo_DE_Reaparicion==[]:
               Tiempo_DE_Reaparicion="Error en la toma de valores"
         break
    

    if Muertes_Asistencias == []:
       Muertes_Asistencias='99/99/99'

    for Nombre in Nombres:
      for i in text_list:
        similitud = fuzz.token_sort_ratio(Nombre, i)
        if similitud >= similitud_minima:
            if numbers !=[]:
             
             Vaolres_Guardados[Nombre]={'Elimin./Asistencias / KO.':Muertes_Asistencias,"Daño Realizado":numbers[0],"tiempo de Supervivencia":Tiempo_DE_Reaparicion }

            else:
              
               Vaolres_Guardados[Nombre]={'Elimin./Asistencias / KO.':Muertes_Asistencias,"Daño Realizado":'Error en toma de valores',"tiempo de Supervivencia":Tiempo_DE_Reaparicion }

    contador+=1


Peloton_Posicion = pytesseract.image_to_string(sección3_superior_masrecortada_top, lang='spa', config='--psm 7 outputbase digits')    


print(f"El peloton Termino Numero {Peloton_Posicion}")

for nombre in Nombres:
        if nombre not in Vaolres_Guardados:
             #Vaolres_Guardados[nombre] = {'Elimin./Asistencias / KO.': '99/99/99',"Daño Realizado":'Error en toma de valores',"tiempo de Supervivencia":"Error en la toma de valores" }
                pass  
        

                #ojo aca arriba 

        if nombre  in Vaolres_Guardados:
         try:
            print(f"{nombre} Daño {Vaolres_Guardados[nombre]['Daño Realizado']} ")  
         except:
            pass
         

print(f"\n")
print(F"{Vaolres_Guardados} \n \n")

#########################################################          LECTURA DE CONTRASTE DE TIEMPOS Y POSICION DE PELOTON    

try:
    a=Determinar_Errores.Tiempos_Peloton_Mejorado(ruta,lenguaje,Nombres)
except:
   pass



print(f"Esto salio de la funcion {a}")              # ESTO MARCA QUE SALIO DEL SCRIPT QUE DETECTA TIEMPO Y POSICION POR LAS DUDAS

if Peloton_Posicion != a['Poscicion del Peloton']:
    if a['Poscicion del Peloton']>20:
       pass
    else:
        Peloton_Posicion=a['Poscicion del Peloton']


      

for namee in Vaolres_Guardados:
    
    tiempoSup = Vaolres_Guardados[namee]['tiempo de Supervivencia']

    if isinstance(tiempoSup, list):

        Vaolres_Guardados[namee]['tiempo de Supervivencia'] = 'Error en la toma de valores'

        tiempoSup = Vaolres_Guardados[namee]['tiempo de Supervivencia']
        
    if tiempoSup == 'Error en la toma de valores':
       
       Vaolres_Guardados[namee]['tiempo de Supervivencia']= a[namee]['tiempo de Supervivencia']

    #if len(tiempoSup)>
    
##################################################################################   MANDA A BASE DE DATOS    if ":" in  Tiempo_Reap
try:
    Peloton_Posicion=int(Peloton_Posicion)
except:
     Peloton_Posicion=99  
if Peloton_Posicion>20 or Peloton_Posicion == 0:
   Peloton_Posicion=99



## ------------------------------------------  IMPRIME LOS VALORES ESPAÑOL Y PONER LOS DE INGLES TAMBIOEN 

print(f"Estos son los datos que se envian: \n {Vaolres_Guardados} + {Peloton_Posicion} \n")


## ------------------------------------------------------------------------------------------   GUARDA LOS VALORES EN LA BASE DE DATOS





  #·························-------------------------    ACA GUARDO TODOS LOS DATOS ERN MYSQL

try:
  Almacenamiento_Definitivo(Peloton_Posicion,Vaolres_Guardados,Ruta_Para_enviar_imagenes,Nombres)         
except:
   print("No pudop enviar los valores a la base de datos por algun problema, trate nuevamente")





print(ruta)











#IndexError: list index out of range


#Pasos a seguir   -  mejorar el reconocimiento    ///           PONER EN LA FUNCION DE ALMACENAMIENTO DE MYSQL QUE ME DEVUELVA EL ID DE LA PARTIDA, DESPUE SCREA OTRO ALGO QUE CON ESE ID PERMITA CORREGIR LSO DATOS, FRENTE A UNA TOMA ERRONEA
#  HAY DATOS QEU COM ELIMINACIONES QUE LSO AMDNA EN AMS DE 20 O ALGO ASI, PONER QEU SEA NULL, POSICION PELOTON EN 99 PONER NULL TRIGER