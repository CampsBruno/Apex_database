import os 
import pyautogui
from datetime import datetime
import keyboard



class Ejecutor():

#    --------------------------------------------------   WHILE TRUE     --------------------------------------------------------

 def Crea_Guarda():

      n=0
      while True:
          if n ==0:
            print("apreta la P")
            n=1
          if keyboard.is_pressed("p"):
              
              
      
              break

      img = pyautogui.screenshot()     
    #   ----------------------------------------------------    FUNCIONES       ---------------------------------------------------     
        
      def Guarda_Que_Vengo(fecha):
        """Guarda la imagen dentro de la carpeta, tiene que buscar el numero de partida que es"""
        
          
        os.chdir(f".\\{fecha}")                   ## aca hay que poner la ubicacion de la partida
        Total=0  
        for i in os.listdir():       ## aca hay que poner la ubicacion de la partida
            
              Total = os.listdir()
              Total=len(Total)
          
          
        return Total


      def Guarde_la_Foto_nomas(Nombre,fecha):
          nombre="Partida N {}".format(Nombre)
          ruta=(f".\\{nombre}.png")                 ## aca hay que poner la ubicacion de la partida
          img.save(ruta)
          return ruta



      







      #-----------------        Obtengo Fecha        -------------------------------
      date=datetime.now()
      fecha = date.strftime('%d-%m-%y')


      print(fecha)

      ## ---------------------------------- TESTEOOO   para verrr

      if not os.path.exists(".\\PARTIDAS"):
            os.mkdir(".\\PARTIDAS")


      #---------------       LISTO TODOS LOS NOMBRES DE LAS CARPETA S EN EL DIRECTORIO    -------------

      os.chdir(".\\PARTIDAS")                                     ## aca hay que poner la ubicacion de la partida

      carpetas=[]
      for i in os.listdir():                          ## aca hay que poner la ubicacion de la partida
          
          if os.path.isdir(i):
              carpetas.append(i)
              





      ############                    CORROBORO SI LA CARPETA EXISTE        #################################
      if fecha in carpetas:
            Partida_Numero=Guarda_Que_Vengo(fecha)            ### seteo el wd y le mando mecha con cuantos archivos hay
            Partida_Numero+=1

            
              
            ruta=Guarde_la_Foto_nomas(Partida_Numero,fecha)  #guarda la imagen, fijate de guardar la hubicacion para despues leerla




      #--------------------------------   CREAR CARPETA  CON ELSE , POR SI NO EXCISTE    ------------------------------------------------------
      else:
                  print("entro a no habia carpeta")

                  
                                               ## aca hay que poner la ubicacion de la partida
                  ruta_actual =os.getcwd()

                  ruta_nueva_carpeta = os.path.join(ruta_actual, fecha) 
                  os.mkdir(ruta_nueva_carpeta)                                              # Creeeeeese la carpeta
                
                  Partida_Numero=Guarda_Que_Vengo(fecha)            ### seteo el wd y le mando mecha con cuantos archivos hay
                  Partida_Numero+=1

            
              
                  ruta=Guarde_la_Foto_nomas(Partida_Numero,fecha)

 
      print(Partida_Numero)
      print(ruta)
      Para_Base_Imagen= f".\PARTIDAS\{fecha}\Partida N {Partida_Numero}.png"
      print(Para_Base_Imagen)
      return ruta, Para_Base_Imagen    
 
 



if __name__ == "__main__":
    ejecutor = Ejecutor()  # Crear una instancia de la clase Ejecutor
    ejecutor.Crea_Guarda()






