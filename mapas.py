import pytesseract
import re
import keyboard
import pyautogui
import cv2
import numpy as np
from fuzzywuzzy import fuzz
from datetime import datetime, timedelta, date, time
import mysql.connector

#----------------------------------------------------------------  EDIT
lenguaje='eng' #   'eng'.

OPEN= "https://apexlegendsstatus.com/current-map/battle_royale/pubs "

user="root"
password="KEnny12345626482"
host="localhost"
database="PRUEBAS_BORRAR"



Maps=["World's Edge",'Storm Point','Broken Moon','Kings Canyon','Olympus']     # ADD MAPS
similitud_minima=80
estructura_Datos={'From  to , ends in  mins','From  to , starts in  hours,  mins.'}



#----------------------------------------------------------------------             FUNCIONES

def corregir_tupla(tupla):
    hora_inicio, hora_fin = tupla
    pattern = re.compile(r'^\d{2}:\d{2}$')
    if not pattern.match(hora_fin) or hora_fin[-1] != '0':
        hora_fin = hora_fin[:-1] + '0'
    TUPLA = (hora_inicio, hora_fin)
    return TUPLA

def obtener_horarios(horario):
    start_end = horario.split(' to ')
    if len(start_end) >= 2:
        return start_end[0].replace('From ', ''), start_end[1].split(',')[0]
    else:
        return None, None

def Ordenar_Fechar_mapas(data):
        c=0
        hora_actual = datetime.now().time()
        fech_actual=datetime.now().strftime('%Y-%m-%d')
        save=True
        for mapa, horarioss in data.items():
            x=len(horarioss)
            if x>c:
                c=x
        para_ver=[]  
        for i in range(c):      
            for mapa, horarios in data.items():
                try:
                      print(f"este esl el horario que se debveria mandar {horarios[i]}")
                      horarios[i]=corregir_tupla(horarios[i])
                      print(horarios)
                except Exception as e:
                      print(e)
                try:                  
                   hora_inicio=datetime.strptime(horarios[i][0], '%H:%M').time()
                   hora_fin=datetime.strptime(horarios[i][1], '%H:%M').time()
                   try:
                        if (hora_inicio > hora_fin) and( hora_fin.strftime('%H:%M') != '00:00' ):  #pone que sea distinto de 00 acaaaaaa               tambien pone que sea 4 digitos y que siemrpe el ultimo dea 0
                                NUEVA_hORA_Fin=hora_inicio.strftime('%H:%M')   #fin de la primera mitad 
                                Hora_fin_Nueva= hora_fin.strftime('%H:%M')
                                Dia_Actual = (NUEVA_hORA_Fin, '23:59')  #primer mitad de la partida
                                Dia_Posterior=('00:00' ,Hora_fin_Nueva)        #Segunda mitad de la partida
                                para_ver.append([mapa, Dia_Actual, fech_actual] )  # agenda la primer mitad
                                fech_actual = datetime.strptime(fech_actual, '%Y-%m-%d')                     
                                fech_actual= fech_actual + timedelta(days=1)
                                fech_actual=fech_actual.strftime('%Y-%m-%d')
                                print("ACA ENTRO AL CORECTOR DE DIAS, LO DEBERIA PARTI Y HACER BIEN MIERDAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
                                print(Dia_Posterior)
                                para_ver.append([mapa, Dia_Posterior, fech_actual] ) #agenda la segunda mitrad
                                save=False
                        elif (hora_fin.strftime('%H:%M'))=='00:00':
                              save=False
                              para_ver.append([mapa, horarios[i], fech_actual] )
                              fech_actual = datetime.strptime(fech_actual, '%Y-%m-%d')                     
                              fech_actual= fech_actual + timedelta(days=1)
                              fech_actual=fech_actual.strftime('%Y-%m-%d')
                   except Exception as e:
                            print(e) 
                except:
                        print("SE paso")
                try:
                        print(mapa,horarios[i])
                        if ((mapa, horarios) not in para_ver) and (save==True):
                            para_ver.append([mapa, horarios[i], fech_actual] )      #ACA MODIFICAR PARA SUBIR A LA BASE DE DATOS
                        save=True 
                except Exception as e:
                            print(e) 
        return para_ver







#-----------------------------------------------------------------------------------    Alamacenaje


class Gurada_Datos_Mapa():
    
    def __init__(self,userr,passwordd,hostt,databasee) -> None:

         self.Base= mysql.connector.connect(
                user=userr,
                password=passwordd,
                host=hostt,
                database=databasee

                )
         self.cursor = self.Base.cursor()

    def Datos_guardados(self):      # Obtengo los datos de la base de datos, ya estandarizados de la fecha actual y una mas
          self.lista_Mapas_Guardados=[]
          try:
            fech_actual=datetime.now().date()
            consulta=("SELECT * FROM Mapas where fecha_mapa>= %s")
            self.cursor.execute(consulta,(fech_actual,))
            self.resultado=self.cursor.fetchall()
          except Exception as e:
               print(e)

          try:
               
               for Datos in self.resultado:
                    ID, Mapa , Hora_inicio, Hora_fin , Fecha_mapa =Datos
                    Hora_inicio = (datetime.min + Hora_inicio).time().strftime('%H:%M')
                    Hora_fin = (datetime.min + Hora_fin).time().strftime('%H:%M')
                    Fecha_mapa=Fecha_mapa.strftime('%Y-%m-%d')
                    
                    agregar=[ID, Mapa , Hora_inicio, Hora_fin , Fecha_mapa]
                    self.lista_Mapas_Guardados.append(agregar)
               
          except:
               pass
          return self.lista_Mapas_Guardados
    
    def Estandarizar_datos(self, datos):                     # estandar de datos ( dar formato)
                    mapa, tupla , fecha = datos
                    inicio, fin = tupla
                    Enviar= [mapa, inicio, fin , fecha ]
                    return Enviar

    def datos_sin_ID(self, datos):
        Enviar=[]
        try:
            
          for i in datos:
                    id, mapa,inicio, fin, fecha = i
                    
                    guardar=[mapa,inicio,fin,fecha]
                    Enviar.append(guardar)
                    
        except Exception as e:
             print(e)
    
        
        
        return Enviar
    

    def Guarda_Valores(self, Datos_Leidos_del_script,Datos_a_contrastar):    # enviar los datos con formato y guardarlos
        try:
                Datos_a_contrastar=self.datos_sin_ID(Datos_a_contrastar)
                print(f"estos son los valores areglados \n \n  {Datos_a_contrastar}")
                for Enviar in Datos_Leidos_del_script:
                        

                        Enviar=self.Estandarizar_datos(Enviar)
                        
                        if Enviar not in Datos_a_contrastar:
                          #  print(f" Este es el dato que logro pasar la barrera \n\n {Enviar}")


                            consulta = ("INSERT INTO Mapas (Mapa, Hora_inicio, Hora_fin, fecha_mapa) VALUES (%s, %s, %s, %s)")
                            self.cursor.execute(consulta,Enviar)
                            self.Base.commit()

        except Exception as e:
             print(e)
        finally:     
            self.cerrar_conexion()


    def cerrar_conexion(self):
                 self.cursor.close()
                 self.Base.close()
          



         
         

          
                        




#-----------------------------------------------------------------------------------------------------------
Diccionario={}

n=0
while True:
          if n ==0:
            print("apreta la P")
            n=1
          if keyboard.is_pressed("p"):
                 break


imagen= pyautogui.screenshot()  

imagen = np.array(imagen)

height, width, _ = imagen.shape
center_width = width // 4  
center_height = height // 1  
imagen = imagen[height // 2 - center_height // 2:height // 2 + center_height // 2,
                      width // 2 - center_width // 2:width // 2 + center_width // 2]


#cv2.imshow("Sección 4", mapimagenas)     Si queres ver que imagenes esta agarrando usa esto
#cv2.waitKey(0)
cv2.destroyAllWindows()


imagen=pytesseract.image_to_string(imagen, lang=lenguaje)  
imagen = imagen.split('\n')
print(imagen)




#-------------------------------------------------------------------------------------------------------------
Mapa_Serach=True
siempre_om=False

for lectura in imagen:
     

     
      
           
          
      if Mapa_Serach== True:      #busca el nombre del mapa para agendar
            for recorte in Maps:
                similitud = fuzz.token_sort_ratio(recorte, lectura)       
                if similitud>= similitud_minima:

                        mapa=lectura
                        Mapa_Serach=False
                        
                    
      else:                                      # busca los numeros pa agendar
                if 'ends' in lectura:
                    
                    Mapa_Serach = True
                    if mapa is not None:
                        if mapa not in Diccionario:
                            
                            Diccionario[mapa] = [lectura]
                        else:
                            Diccionario[mapa].append(lectura)    #MODIFICAR, QUE SOLOVEA SI ESTA LA KEY SI NO ESTA QUE LA AGREGUE Y SI ESTA QUE APENDEE EL MAPA
                elif 'starts' in lectura:
                    
                    Mapa_Serach = True
                    if mapa is not None:
                        if mapa not in Diccionario:
                            
                            Diccionario[mapa] = [lectura]
                        else:
                            
                            Diccionario[mapa].append(lectura)





# Crear una nueva estructura de datos con las claves y los horarios de inicio y fin
nuevos_datos = {}
for mapa, horarios in Diccionario.items():
    nuevos_datos[mapa] = [obtener_horarios(h) for h in horarios if h]








mapas_con_fecha_ordenados = Ordenar_Fechar_mapas(nuevos_datos)



print(f" Este es el final del Script \n {mapas_con_fecha_ordenados}")





obtengo_datos=Gurada_Datos_Mapa(user,password,host,database)
datos=obtengo_datos.Datos_guardados()
#print(f"DATOs de la base de datosd \n {datos}")
#print(f"\n \n Datos de lectura  {mapas_con_fecha_ordenados}")

obtengo_datos.Guarda_Valores(mapas_con_fecha_ordenados,datos)
obtengo_datos.cerrar_conexion()



