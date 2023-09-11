
import pytesseract
import re
from PIL import Image
import cv2
import numpy as np
from fuzzywuzzy import fuzz
import pyautogui
import keyboard
from Moduls.Almacena_Imagenes import Ejecutor

          
          
          
class Determinar_Errores():          
          
              
              
              
    def Tiempos_Peloton_Mejorado(ruten,lenguaje,Names):
              

                language=lenguaje
                ruta=ruten     # ruta del archivo

                Nombres= Names
                
                if language == 'spa' :
                    Tiempo_SUPERvivencia=['Tiempo de supervivencia']
                else:
                      Tiempo_SUPERvivencia=['Survival Time']  

                
                Vaolres_Guardados={}  
                def extraer_numeros(cadena):
                    
                    patron = r"[-+]?\d*\.\d+|\d+"
                    numeros = re.findall(patron, cadena)
                    
                    
                    numeros = [int(numero) for numero in numeros]
                    
                    return numeros



                def extraer_numeros_peloton(cadena):
                        patron = r"(?<!\d)-?\d+(?!\d)"
                        numeros = re.findall(patron, cadena)
                        
                        numeros_validos = []
                        for numero in numeros:
                            try:
                                numeros_validos.append(int(numero))
                            except ValueError:
                                pass
                        
                        return numeros_validos




                def extraer_dañoss(cadena):
                    # Expresión regular para encontrar números enteros y decimales
                    patron = r"[-+]?\d*\.\d+|\d+"
                    numeros = re.findall(patron, cadena)
                    if len(numeros)==1:
                        
                        a=[]
                        v=0
                        for i in numeros:
                            a.append(i)
                            if len(a)==3:   
                                numeros= a[0]+ ":" +  a[1] + a[2] 
                                print(numeros)
                            if len(a)==4: 
                                numeros= a[0]+    a[1] +":" + a[2] + a[3]
                    elif len(numeros)==2:
                        numeros=numeros[0]+":" +numeros[1]
                    

                    
                    return numeros








                
                Eliminaciones_Asistencias=['Elimin./Asistencias / K.O.']
                #daño_infli=["Daños infligidos"]
                similitud_minima = 65
                simillitud_Megaminima = 45


                

                img = cv2.imread(R"{}".format(ruta))    # CARGA IMAGEN DESDE EL CODIGO NUEVO


                #--------------------------------------------------------------------------------------------------------------------------------


                img = np.array(img)
                


                # Convierte la imagen a escala de grises
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

                # Aplica un filtro de suavizado para eliminar el ruido
                blur = cv2.GaussianBlur(gray, (5, 5), 0)   






                





                # Ajusta el contraste y brillo de la imagen
                alpha = 1.5
                beta = 0
                adjusted = cv2.convertScaleAbs(blur, alpha=alpha, beta=beta)





                Tiempo_DE_Reaparicion=[]
                numbers=[]
               
                height, width = adjusted.shape[:2]
                Superior=adjusted[:height//3, :]

                img = adjusted[height//4:, :]
                # Dividir la imagen en tres secciones verticales iguales
                seccion1 = adjusted[:, 0:width//3]
                seccion2 = adjusted[:, width//3:2*width//3]
                seccion3 = adjusted[:, 2*width//3:]

                seccionSuperior=adjusted[:, 2*width//3:]



                #######################Recorte de la 1
                height, width= seccion1.shape
                sección1_superior = seccion1[380: int(height*9), 50:width]                                                    #seccion2[0:height//1, 0:width] #
                sección1_superior_masrecortada = sección1_superior[:, 0:width//6*3]    ## MODIFIQUE ESTO sección1_superior[200:610   PONE el 200:610 en :  solo sin nada y vuelve a lo normal



                #######################Recorte de la 2
                height, width = seccion2.shape
                sección2_superior = seccion2[250: int(height*3), 100:width//3*9]  
                sección2_superior_masrecortada = sección2_superior[:, 0:width//3]


                ################################################Recorte de la 3

                height, width  = seccion3.shape
                sección3_superior = seccion3[250: int(height*3), 0:width]  
                sección3_superior_masrecortada = sección3_superior[:, 0:width//7*3]


                #######################D  Solo del PELOTON RESTAQNTE
                height, width = seccionSuperior.shape

                sección3_superior_top = seccionSuperior[20:int(height*10)-10, 0:width]
                sección3_superior_masrecortada_top = sección3_superior_top[125:int(height/4)-100, 230:width//7*3]


                

                cv2.waitKey(0)
                cv2.destroyAllWindows()

                Secciones=[sección1_superior_masrecortada,sección2_superior_masrecortada,sección3_superior_masrecortada]
                numbers=[]
                contador=0
                Muertes_Asistencias=0
                ##################################################################   OEM

                oem = 2

                ###############################

                for i in Secciones:

                      

                    text = pytesseract.image_to_string(i, lang='spa', config=f'--oem {oem}')  #Proba esto a ver si mejora los resultados
                    text_list = text.split('\n')
                    #print(text_list)
                    

                
                    
                    
                    
                    
                    
                    b=False
                    for Tiempo_Reap in text_list:
                        
                        similitud = fuzz.token_sort_ratio(Tiempo_SUPERvivencia, Tiempo_Reap)

                        if b==True:
                            if ":" in  Tiempo_Reap:
                                
                                try:
                                 Tiempo_DE_Reaparicion=extraer_dañoss(Tiempo_Reap)  
                                except:
                                     print("error en tiempo de reaparicion de 'Tiempo_Peolton.py', busca la funcion fallada") 
                                if len(Tiempo_DE_Reaparicion)> 10:
                                     Tiempo_DE_Reaparicion=[]

                                break

                        if similitud >= similitud_minima:
                            b=True

                    











                    
                    for Nombre in Nombres:
                        for i in text_list:
                            similitud = fuzz.token_sort_ratio(Nombre, i)
                            if similitud >= similitud_minima:
                                if Tiempo_DE_Reaparicion != []:
                                   
                                    Vaolres_Guardados[Nombre]={"tiempo de Supervivencia":Tiempo_DE_Reaparicion }
                                else:
                                                    
                                                    Vaolres_Guardados[Nombre]={"tiempo de Supervivencia":'Error en la toma de valores' }





                    

                    contador+=1


                



    
                
                Posicion_Peloton = pytesseract.image_to_string(sección3_superior_masrecortada_top, lang='spa', config='--psm 7 outputbase digits')

                


                try:
                      Posicion_Peloton=extraer_numeros_peloton(Posicion_Peloton)
                except:
                     Posicion_Peloton=99
                try:
                     Posicion_Peloton=Posicion_Peloton[0]

                     Vaolres_Guardados["Poscicion del Peloton"]=Posicion_Peloton
                except:
                     Vaolres_Guardados["Poscicion del Peloton"]=99

                for nombre in Nombres:
                    if nombre not in Vaolres_Guardados:
                        Vaolres_Guardados[nombre] = {"tiempo de Supervivencia":'Error en la toma de valores' }


                return Vaolres_Guardados

              
if __name__== "__main__":
     a=Determinar_Errores.Tiempos_Peloton_Mejorado()
     print(a)