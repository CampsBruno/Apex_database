
import mysql.connector 
import pandas as pd
import os
from datetime import datetime







####################################################################           modify parameters                        #########################################################


Base= mysql.connector.connect(
          user="modify this",       #-------------  Modify,
          password="modify this",       #-------------  Modify,
          host="modify this",       #-------------  Modify
          database="Apex_DB"

          )










################################################################################################################################################



cursor = Base.cursor()
#------------------------------------------------------------------------------------------       Funciones
def ruta_imagen(n_partida):
    try:
        n_partida= n_partida[0][1]
        Consulta= ('select ruta_imagen from partidas where matchid = %s')
    except Exception as e:
        print(e)
    try:
        valores= int(n_partida)
    except Exception as e:
        print(f" Fallo en la toma de la ruta de la imagen {e}")
    try:
        cursor.execute(Consulta,(valores,))
        respuesta= cursor.fetchall()
    except Exception as e:
        print(f" Fallo en la toma de valores {e}")
        respuesta = e
    return respuesta
#---------------------------------------------------------------------------------------       Fin Funciones 

try:

    constulta= ("select ID,matchid,error_datos  from Resultados_Partida where error_datos is not null")
    try:
        cursor.execute(constulta)
        Problemas =cursor.fetchall()
        
    except Exception as e:
        print(e)

    try:
        Tabla= pd.DataFrame(Problemas, columns=["ID","MatchId","Codigo_Error"])

        print(Tabla)
    except Exception as e:
        print(e)

    Trabajo_Con=int(Tabla['ID'][0])

    
    
    Consulta= ('Select re.ID,re.matchID, f.Nombre,re.Eliminacion,re.asistencia, re.kills, re.daño, re.tiempo, re.error_datos from Resultados_Partida  re join jugador f on f.PID = re.PlayerID where ID = %s and error_datos is not null')  #TIME_FORMAT(re.TIEMPO, '%i:%s')as tiempo
    cursor.execute(Consulta,(Trabajo_Con,))
    Devuelve= cursor.fetchall()


    print(" ARRIBA ESTA LA LISTA DE ERRORES EN LAS PARTIDAS, ABAJO ESTAN LOS VALORES A CORREGIR DE LA IMAGEN QUE SE ABRE \n")

    respuesta = ruta_imagen(Devuelve)

    #print(respuesta)

    ruta = respuesta[0][0]

    Devuelve= list(Devuelve[0])

    #print(Devuelve)
    Correccion=[]
    n=0
    for i in Devuelve:
        if i== None :
            Correccion.append(n)

        n+=1

    Nombres_Columnas=["ID","MatchID","PlayerID","Eliminacion","Asistencia","Kills","Daño","Tiempo","Error_Datos"]



    Datos_Tot= pd.DataFrame([Devuelve], columns=Nombres_Columnas)

    print(f"{Datos_Tot} \n")

    print(f"Vamos a Corregir los valores de {Datos_Tot['PlayerID'][0]} \n")

    #-----------------------------------------------------------------------------------------------------  Abre la imagen



    #directorio_actual = os.getcwd()
    #print("Directorio de trabajo actual:", directorio_actual)
   # ruta_imagen = os.path.join(directorio_actual,ruta )



    os.startfile(ruta)

    for i in Correccion:
        A_Corregir= Nombres_Columnas[i]
        while True:
            Corregido=str(input(f"Corregi el  {A_Corregir}:  "))

            confirmo=str(input(f"El valor es de {Corregido} Confirma con Y / N  / C  (Cancel): ").lower())
            
            if confirmo== "y":
                if A_Corregir == "Tiempo":
                    Corregido = Corregido
                    Corregido = datetime.strptime(Corregido, '%M:%S')

                    try:
                        constulta=(f"UPDATE Resultados_Partida SET {A_Corregir} = %s WHERE ID = {Trabajo_Con} ")
                        cursor.execute(constulta, (Corregido,) )

                    except Exception as e:
                        print(e)
                            
                    break
                
                else:
                    constulta=(f"UPDATE Resultados_Partida SET {A_Corregir} = %s WHERE ID = {Trabajo_Con} ")
                    cursor.execute(constulta, (Corregido,) )
                #Base.commit()
                break
            
            if confirmo== "c":
                break

####------------------------------------------------------------------------------------------------------------
####  aca voy a poner la parte de los pdi de partidas






            
    
 ## ----------------------------------------------------------------------------------------------       
   
    
except Exception as e:
    print(" \n No hay partidas en Resultados_partidas para corregir")
    print(e)

try:
        nueva_consulta= "SELECT * FROM partidas WHERE PID1 IS NULL AND PID2 IS NULL AND PID3 IS NULL "
        cursor.execute(nueva_consulta,())
        nueva_respueesta=cursor.fetchall()
        MatchID_Delete=int(nueva_respueesta[0][0])
        Segunda_ruta=nueva_respueesta[0][7]
        print(f"la ruta es esta : {Segunda_ruta}")
        try:
            os.startfile(Segunda_ruta) 
        except Exception as e:
            print(f"No se pudo abrir el archivo: {e}")    
        while True:
            corrigiendo_datos=input("No player appears in this image.\n  Do we delete the image and records? \n  Y/N or C (Cancel)").lower()
            if  corrigiendo_datos == "y":
                  
                  if os.path.exists(Segunda_ruta):
                        # Eliminamos el archivo   
                      try:          
                        os.remove(Segunda_ruta)    # ABAJO DE ESTO HAYQ UE PONER QUE APARTE DE BORRAR LA IMAGEN ELIMINE LOS REGISTROS DE MYSQL
                      except Exception as e:
                        print(f"Could not delete file: {e}")  

                      try:
                        consulta="delete from partidas where matchid=%s"
                        cursor.execute(consulta,(MatchID_Delete,))
                      except Exception as e:
                        print(f"Could not delete database record: {e}")
                    
                      break
                  else:
                      try: 
                        consulta="delete from partidas where matchid=%s"
                        cursor.execute(consulta,(MatchID_Delete,))
                      except Exception as e:
                        print(f"Could not delete database record: {e}")
                    
                      break
            else:
                break# SI FUE UN ERROR TIEN EQUE AGREGAR A RESULTADOS PARTIDA LOS VALORES
except Exception as e:
    print(f"No hay partidas Nulas para corregir")
    print("There are no Null games to correct \n")

Base.commit()    

try:
    consulta="SELECT * FROM Partidas WHERE Posicion_Peloton= 99"
    cursor.execute(consulta,())
    Partidas_Con_error_peloton=cursor.fetchall()
    ID_Partidas_Con_error_peloton=Partidas_Con_error_peloton[0][0]
    Ruta_de_error_peloton=Partidas_Con_error_peloton[0][7]
    try:
            os.startfile(Ruta_de_error_peloton) 
    except Exception as e:
            print(f"Could not open file: {e}")   
    posicion_peloton_corregido=int(input("Insert the Squad Position:  " ))
    respuesta=input(f"The inserted value is: {posicion_peloton_corregido} \n Is this value correct? Y/N or C (cancel)").lower()
    while True:
        if respuesta == "y":
            try:
                constulta=(f"UPDATE Partidas SET Posicion_Peloton ={posicion_peloton_corregido}  WHERE MatchID = {ID_Partidas_Con_error_peloton} ")
                cursor.execute(constulta,())

            except Exception as e:
                    print(e)     
            break
        elif respuesta == "n":
            posicion_peloton_corregido=int(input("Insert the Squad Position"))
            respuesta=input(f"The inserted value is: {posicion_peloton_corregido} \n Is this value correct? Y/N or C (cancel)").lower()
        else:
            break

except Exception as e:
    print(e)

Base.commit()
cursor.close()
Base.close()



