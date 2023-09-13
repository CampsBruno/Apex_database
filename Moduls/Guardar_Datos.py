import mysql.connector
from datetime import time
from datetime import datetime



def Almacenamiento_Definitivo (Peloton_Posicion,Vaolres_Guardadoss,Ruta_Imagenn,names_players ):



  try:  ##------------------------------------------------------    MODIFY    --------------------------------------------------#############################################################################
          Base= mysql.connector.connect(
          user="modify this",       #-------------  Modify,
          password="modify this",       #-------------  Modify,
          host="modify this",       #-------------  Modify
          database="Apex_DB"



          
## ######################################################################################################################################################################################################################################
          )

          cursor=Base.cursor()

          Posicion_Pelotonn=Peloton_Posicion
          Vaolres_Guardados=Vaolres_Guardadoss
          Ruta_Imagen=Ruta_Imagenn
            
                     

#  # --------------------------------------- ACA VOY A AGREGAR LOS VALORES DE LA NUEVA BASE, SON LOS EXPERIMIENTOS  (1/2)    
# 
          Nombres_pLAYERS=names_players
#            
          consulta= "select * from Jugador"       # ----------- parte de buscar si los jugadores estan en la base de datos 
          cursor.execute(consulta)
          id_nombres=cursor.fetchall()


          nombres_guardados = [i[1] for i in id_nombres if i]

          if nombres_guardados == []:              # --------------------------   los agrega si no estan 
              for search_player in Nombres_pLAYERS:
                    consulta="INSERT INTO jugador(nombre) VALUE(%s)"
                    cursor.execute(consulta,(search_player,))
                    

          else:
              save_data=False
              for name_in_list in Nombres_pLAYERS:                        #--  corroboor dentro de la lista cada nombre si estas en lña base de datos/ si no esta lo agrega y si esta sigue su curso 

                  for nombres_enbase_datos in nombres_guardados:
                      if name_in_list in nombres_enbase_datos:
                          save_data=False

                          break
                      if name_in_list not in nombres_enbase_datos:
                          save_data=True

                  if save_data==True:
                          print(name_in_list, "no esta almacenado mpapu pero ahi lo soluciono")
                          consulta="INSERT INTO  Jugador(Nombre) value(%s)"
                          cursor.execute(consulta,(name_in_list,))   
                          save_data=False                                              #----     terminamos con la parte de agregar jugadroes
              #-    busca el ide de los jugadores recien agregados 
               

          Requeridos=[]
          names_for_id=Vaolres_Guardados                              #busca los id de los jugadores del diccionario en la base de datos  
        
          try:
                          for a in  names_for_id:
                            solicitud=("SELECT PID from Jugador Where Nombre = (%s) ")
                            cursor.execute(solicitud,(a,))

                            playerID = cursor.fetchall()
                            Requeridos.append(playerID[0][0])                

          except Exception as e:
                                print(f"Error en solicitud de PID\n  {e}")




               #    Almacena los datos en la base de datos de los jugadores que recein llame 

          ddatos_enviar=[None,None,None]

          try:
                for indice in range(0,len(Requeridos)):
                      ddatos_enviar[indice]=Requeridos[indice]
          except:
            pass

          #print(f"Este es el dato a enviaR  {ddatos_enviar}")
          try:
              pedido=("INSERT INTO partidas(PID1,PID2,PID3,Posicion_Peloton,Ruta_Imagen) VALUES(%s,%s,%s,%s,%s)")
              numeros= (ddatos_enviar[0],ddatos_enviar[1],ddatos_enviar[2],Posicion_Pelotonn,Ruta_Imagen) 
              cursor.execute(pedido,numeros)
              ultimoID=cursor.lastrowid 
          except Exception as e:
                print(e)

         

# ---------------------------------------------    FINB DELK EXPERIMENTO LO DE ABAJO ES LO QUE HABIA ANTES (2/2)


          
           




          

          ultimoID=cursor.lastrowid    

          



          #######################################################################  Modifica todo pero para la proxima tabla

          for i in Vaolres_Guardados:
                  
                  x=(Vaolres_Guardados[i]['Elimin./Asistencias / KO.']).split("/")
                  KO=99
                  Asistencia=99
                  Eliminacion=99
                  if len(x)==3:
                        try:
                          Eliminacion=int(x[0])
                          Asistencia= int(x[1])
                          KO=int(x[2])

                        except ValueError:
                                pass
                  else:
                          print("Error en toma")
#-------------------------------------------------------------------------------------------------------------------- SI HAY ERROR SIMPLEMENTE SACA ESTO
                  if Eliminacion>20 and Eliminacion!=99:
                        Eliminacion=99

                  if Asistencia>20 and Asistencia!=99:
                        Asistencia=99

                  if KO>20 and KO!=99:
                               KO=99

 #-------------------------------------------------------------------------------------------------------------------- FIN DE EXPERIMENTO                       
                  a= [i]
                  try:
                      solicitud=("SELECT PID from Jugador Where Nombre = (%s) ")
                      cursor.execute(solicitud,a)                
                  except:
                          print("Error en solicitud de PID")
                          
                  playerID = cursor.fetchall()
                  playerID = playerID[0][0]

                
                  daño=Vaolres_Guardados[i]['Daño Realizado']    ## DAÑOOOO

                  if daño == 'Error en toma de valores':
                        daño= "9999"

                  Tiempo_Peloton=Vaolres_Guardados[i]['tiempo de Supervivencia']   ## PONER SI DAÑO VIOLENTO  = 'Error' SETEALO EN 9999
                  
                  if Tiempo_Peloton== 'Error en la toma de valores':
                      
                              try:
                                  Tiempo_Peloton= "59:59"
                                  tiempo_peloton = Tiempo_Peloton
                                  Tiempo_Pelotone = datetime.strptime(tiempo_peloton, '%M:%S')

                                  Orden= ("INSERT INTO Resultados_Partida (matchid, playerid,eliminacion,asistencia,kills,daño,tiempo) VALUES (%s,%s,%s,%s,%s,%s,%s) ")

                                  numeros_insertar= (ultimoID,playerID,Eliminacion,Asistencia,KO,daño,Tiempo_Pelotone)


                                  cursor.execute(Orden,numeros_insertar)

                              except:
                                  print(f"Error en tiempo de peloton = toma de valores fallida {ultimoID} ,JUGADOR {playerID} ,{'00:59:59'}")
                                  try:
                                      
                                      Orden= ("INSERT INTO Resultados_Partida (matchid, playerid) VALUES (%s,%s) ")
                                      numeros_insertar= (ultimoID,playerID)
                                      cursor.execute(Orden,numeros_insertar)
                                  except Exception  as e:
                                    print(f"Volvio a dar error  {ultimoID} ,JUGADOR {playerID} ,{'00:59:59'}")
                                    print (e)

                  else:    

                              try:  
                                  tiempo_peloton = str(Tiempo_Peloton)
                                  
                                  Tiempo_Pelotoni = datetime.strptime(tiempo_peloton, '%M:%S')

                                  print(i,Eliminacion,Asistencia,KO,Tiempo_Peloton)

                                  Orden= ("INSERT INTO Resultados_Partida (matchid, playerid,eliminacion,asistencia,kills,daño,tiempo) VALUES (%s,%s,%s,%s,%s,%s,%s) ")

                                  numeros_insertar= (ultimoID,playerID,Eliminacion,Asistencia,KO,daño,Tiempo_Pelotoni)


                                  cursor.execute(Orden,numeros_insertar)
                              except Exception as e:
                                print("Fallo el envio de datos a Resultados_Partida", e )








          Base.commit()
          cursor.close()
          Base.close()

  except Exception as e:
         print(e)



# armar el data science



if __name__ == "__main__":
     Almacenamiento_Definitivo ()

