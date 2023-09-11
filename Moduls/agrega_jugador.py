import mysql.connector


valores_guardados={'cheliRp': {'Elimin./Asistencias / KO.': '3/1/3', 'Daño Realizado': 400, 'tiempo de Supervivencia': '7:02'}, 
                   '[Vpr]-Sicario': {'Elimin./Asistencias / KO.': '2/2/2', 'Daño Realizado': 344, 'tiempo de Supervivencia': '7:20'},
                   'Kaleroth': {'Elimin./Asistencias / KO.': '2/3/2', 'Daño Realizado': 715, 'tiempo de Supervivencia': '7:20'}}





user="root"
password="KEnny12345626482"
host="localhost"
database="PRUEBAS_BORRAR"


nombre_Testeo= ["[Vpr]-Sicario","cheliRp","Kaleroth"] 





base= mysql.connector.connect(user="root",
            password="KEnny12345626482",
            host="localhost",
            database="PRUEBAS_BORRAR"
                              )


cursor=base.cursor()





##############################################################################     busca si el jugador existe en la base de datos y si no esta lo agrega

consulta= "select * from Jugador"       # -----------BUSCA EN BASE
cursor.execute(consulta)
id_nombres=cursor.fetchall()


nombres_guardados = [i[1] for i in id_nombres if i]

if nombres_guardados == []:
     for append in nombre_Testeo:
          consulta="INSERT INTO jugador(nombre) VALUE(%s)"
          cursor.execute(consulta,(append,))
          

else:
    save_data=False
    for name_in_list in nombre_Testeo:

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
                save_data=False       




#-----------------------------------------------------------------------------------------------------------------------------



###################################################################     BUSCA LOS IDE DE DE LAS KEY DEL DICCIONARIO valores_guardados  ENVIADO POR MAIN

def Return_ID(nombre_Testeoo):
     

     Requeridos=[]
     names_for_id=nombre_Testeoo
     
     try:
                    for a in  names_for_id:
                      solicitud=("SELECT PID from Jugador Where Nombre = (%s) ")
                      cursor.execute(solicitud,(a,))

                      playerID = cursor.fetchall()
                      Requeridos.append(playerID[0][0])                

     except Exception as e:
                          print(f"Error en solicitud de PID\n  {e}")

     return Requeridos

impreison=Return_ID(valores_guardados)
print(impreison)

###-------------------------------------------------------------------   ----------------------------------------------------------------------------
# 
# 
# ############################################################################     GUARDA TODOS LSO DATOS EN PARTIDAS (CON LOS PDI SOLICITADOS Y SI ESTOS NO ESTAN MANDA UN NONE) 
Posicion_Pelotonn=15
Ruta_Imagen="ruta?imagen"

ddatos_enviar=[None,None,None]

try:
       for indice in range(0,len(impreison)):
            ddatos_enviar[indice]=impreison[indice]
except:
  pass

print(f"Este es el dato a enviaR  {ddatos_enviar}")
try:
    pedido=("INSERT INTO partidas(PID1,PID2,PID3,Posicion_Peloton,Ruta_Imagen) VALUES(%s,%s,%s,%s,%s)")
    numeros= (ddatos_enviar[0],ddatos_enviar[1],ddatos_enviar[2],Posicion_Pelotonn,Ruta_Imagen) 
    cursor.execute(pedido,numeros) 
except Exception as e:
       print(e)


##-----------------------------------------------------------------------------------------------------------------------------------------------

base.commit()
base.close()




