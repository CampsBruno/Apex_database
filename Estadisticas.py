import pandas as pd
import mysql.connector
from datetime import datetime
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np
################################################################   MODIFICABLES


orden = ['[Vpr]-Sicario', 'cheliRp', 'Kaleroth']




#######################################################
class Estadistica():

        def __init__(self,userr,paswordd,hostt,databasee):
        
                  self.Base= mysql.connector.connect(
                                        user=userr,
                                        password=paswordd,
                                        host=hostt,
                                        database=databasee

                                        )

                  self.cursor = self.Base.cursor()


        def Pedido(self):

                try:
                        Consulta= "select * from Resultados_Partida"

                        #valores= ""
                        self.cursor.execute(Consulta)  #(valores,)
                        self.resultado=self.cursor.fetchall()
                        

                except Exception as e:
                        print(e)
                
                return self.resultado


        #Base.commit()
        def cerrar_conexion(self):
                 self.cursor.close()
                 self.Base.close()




        def Obtener_datos(self,Dias=None):
             """Poner el dia  del cual sacar promedio, por defecto toma todos los valores historicos """
             self.resultado="no funco"
             if Dias is None:
                try:
                        Consulta=("SELECT E.id,E.MATCHID,L.NOMBRE, E.Eliminacion,E.ASISTENCIA,E.KILLS,E.DAÑO, TIME_FORMAT(E.TIEMPO, '%i:%s')as tiempo ,S.Dia_Numero FROM Resultados_Partida E JOIN Partidas S ON S.MATCHID=E.MATCHID JOIN JUGADOR AS L ON L.PID= E.PLAYERID")
                        self.cursor.execute(Consulta)  #(valores,)
                        self.resultado=self.cursor.fetchall()
                        
                except Exception as e:
                        print (e)

             else:
                try:
                       
                        Consulta=f"SELECT E.id,E.MATCHID,L.NOMBRE, E.Eliminacion,E.ASISTENCIA,E.KILLS,E.DAÑO, TIME_FORMAT(E.TIEMPO, '%i:%s')as tiempo ,S.Dia_Numero FROM Resultados_Partida E JOIN Partidas S ON S.MATCHID=E.MATCHID JOIN JUGADOR AS L ON L.PID= E.PLAYERID where s.Dia_Numero= {Dias}"
                        
                        self.cursor.execute(Consulta)  #(valores,)
                        self.resultado=self.cursor.fetchall()
                       
                except Exception as e: 
                        print(e)
#########################################
# 
#                # Convert the list to a DataFrame
             column_names = ["id", "MATCHID", "NOMBRE", "Eliminacion", "ASISTENCIA", "KILLS", "DAÑO", "tiempo", "Dia_Numero"]
             self.resultado = pd.DataFrame(self.resultado, columns=column_names)

                # Convert the 'tiempo' column to a numeric data type (seconds)
             self.resultado['tiempo'] = self.resultado['tiempo'].apply(lambda x: int(x.split(':')[0]) * 60 + int(x.split(':')[1]) if x is not None else None)


         
         
 ##################################################        
             return self.resultado




        def Exportar_Datos(self):
                try:
                        Consulta=("select id,MatchID,Nombre,Eliminaciones,Asistencias,KO,Daño,Tiempo_Supervivencia,Posicion_Peloton,Fecha,Hora,Dias,Fallo_Valores,Mapa from Tabla_definitiva")
                        self.cursor.execute(Consulta)  #(valores,)
                        self.resultado=self.cursor.fetchall()
                        
                except Exception as e:
                        print (e)               
   

                try:
                        column_names = ["id", "MatchID", "Nombre", "Eliminaciones", "Asistencias", "KO", 
                        "Daño", "Tiempo_Supervivencia", "Posicion_Peloton", "Fecha", 
                        "Hora", "Dias", "Fallo_Valores", "Mapa"]
                        self.df = pd.DataFrame(self.resultado, columns=column_names)
                        self.df['Hora'] = self.df['Hora'].apply(lambda x: str(x).split()[-1])  
                        self.df['Tiempo_Supervivencia'] = self.df['Tiempo_Supervivencia'].apply(lambda x: str(x).split()[-1])  
                        print(self.df)

                        self.df.to_excel('.\\Exportar\\de_exportacion.xlsx', index=False)
                except Exception as e:
                        print (e)  
                return self.resultado,column_names
        
        
        
        def filtrar_datos_por_jugador(self, Datos_ingresados):
                lista_de_datos={}
                for nombre_jugador in Datos_ingresados:
                        datos_jugador = self.resultado[self.resultado['NOMBRE'] == nombre_jugador]
                        lista_de_datos[nombre_jugador]=datos_jugador
                return lista_de_datos


#  ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
        user="root"                      #-------------------------------------------------------------  aca  a sacar
        password="KEnny12345626482"
        host="localhost"
        database="PRUEBAS_BORRAR"
        estadistica = Estadistica(user, password, host, database)
        respuesta=estadistica.Obtener_datos(5)
        #estadistica.Exportar_Datos()     ##                              Exportar datos
        
        
        estadistica.cerrar_conexion()









aa=estadistica.filtrar_datos_por_jugador(orden)
print("abajo es lo que salio")
print(aa["cheliRp"]["ASISTENCIA"])   #guarda que salio










#########################  experimentos





#print(nombre)
dataframe = pd.DataFrame(respuesta)

dataframe = dataframe.sort_values(by='MATCHID')
dataframe = dataframe.reset_index(drop=True)
#print(dataframe)
datos=respuesta


# Obtener los datos del dataframe
partidas = dataframe['MATCHID'].values
danio = dataframe['DAÑO'].values
jugadores = dataframe['NOMBRE'].unique()
eliminaciones = dataframe['Eliminacion'].values
asistencias = dataframe['ASISTENCIA'].values
kills = dataframe['KILLS'].values

print(dataframe)
print(kills)
def grafiquese(dataframe):
        
        fig, ax = plt.subplots()

        # Iterar sobre los jugadores y graficar las líneas correspondientes
        for jugador in jugadores:
                mask = dataframe[2] == jugador
                ax.plot(partidas[mask], danio[mask], label=jugador)

        # Etiquetas de los ejes
        ax.set_xlabel('Partidas')
        ax.set_ylabel('Daño')

        # Título del gráfico
        ax.set_title('Daño en función de las partidas jugadas')

        # Leyenda
        ax.legend()
        ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True))
        # Mostrar la gráfica
        plt.show()




def Grafico_torta(dataframe):
                print(dataframe)
                
                total_danio = dataframe.groupby(2)[6].sum()

                # Ordenar el dataframe según el orden deseado
                total_danio = total_danio.sort_values(ascending=False)

                # Graficar el gráfico de torta
                plt.pie(total_danio, labels=total_danio.index, autopct='%1.1f%%')

                # Título del gráfico
                plt.title('Distribución del daño por jugador')

                # Mostrar el gráfico
                plt.show()

                #print(dataframe)





def  Puntual(dataframe):
        jugadores = dataframe['NOMBRE'].unique()

        # Crear la figura y los ejes
        fig, ax = plt.subplots()

        # Iterar sobre los jugadores y graficar los puntos correspondientes
        for jugador in jugadores:
                mask = dataframe[2] == jugador
                ax.scatter(dataframe[1][mask], dataframe[6][mask], label=jugador)

        # Etiquetas de los ejes
        ax.set_xlabel('Partidas')
        ax.set_ylabel('Daño')

        # Título del gráfico
        ax.set_title('Daño en función de las partidas jugadas')

        # Leyenda
        ax.legend()
        ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True))
        # Mostrar la gráfica
        plt.show()






def Grafico_torta_eliminacioens(dataframe):

                total_danio = dataframe.groupby(2)[4].sum()

                # Ordenar el dataframe según el orden deseado
                total_danio = total_danio.sort_values(ascending=False)

                # Graficar el gráfico de torta
                plt.pie(total_danio, labels=total_danio.index, autopct='%1.1f%%')

                # Título del gráfico
                plt.title('Eliminaciones del equipo')

                # Mostrar el gráfico
                plt.show()





def Obtener_DataMedia(orden,dataframe):

        # Agrupar el dataframe por jugador y calcular el promedio de cada columna
        dataframe_mean = dataframe.groupby('NOMBRE').mean()


        total_danio = dataframe.groupby('NOMBRE')['Eliminacion'].sum()

        # Obtener los jugadores únicos
        jugadores = dataframe['NOMBRE'].unique()

        #---------------------
        
        # Reordenar el dataframe según el orden deseado
        dataframe_mean = dataframe_mean.reindex(orden)
        
        return dataframe_mean
#------------------


dataframe_mean= Obtener_DataMedia(orden,dataframe)
print(dataframe_mean)
# Crear la figura y los ejes
fig, ax = plt.subplots()

# Definir el ancho de las barras
bar_width = 0.2

# Definir las posiciones de las barras
r1 = np.arange(len(jugadores))
r2 = [x + bar_width for x in r1]
r3 = [x + bar_width for x in r2]
r4 = [x + bar_width for x in r3]


# Crear un segundo objeto de ejes que comparta el eje X
ax2 = ax.twinx()

# Graficar las barras para cada columna
ax.bar(r1, dataframe_mean['Eliminacion'], width=bar_width, label='Eliminaciones')
ax.bar(r2, dataframe_mean['ASISTENCIA'], width=bar_width, label='Asistencias')
ax.bar(r3, dataframe_mean['KILLS'], width=bar_width, label='Ko')
ax2.bar(r4, dataframe_mean['DAÑO'], width=bar_width, label='Daño', color='red')

# Etiquetas del eje X
ax.set_xticks([r + bar_width for r in range(len(jugadores))])
ax.set_xticklabels(orden)


# Definir los valores que quieras mostrar en el eje Y
valores = [0.1, 1, 10, 100, 1000]

# Asignar los valores al eje Y
ax.set_yticks(valores)
ax.set_yticklabels(valores)

# Definir los límites inferior y superior de la escala logarítmica
ax.set_ylim(0.1, 1000)

# Etiquetas de los ejes
ax.set_xlabel('Jugador')
ax.set_ylabel('Promedio')

# Usar una escala logarítmica en el eje Y
ax.set_yscale('log')

# Título del gráfico
ax.set_title('Rendimiento promedio por jugador')

# Leyenda
ax.legend()

# Mostrar el gráfico
#plt.show()

def Grafico_barras(dataframe):
    # Agrupar el dataframe por jugador y calcular el total de cada columna
    dataframe_total = dataframe.groupby('NOMBRE').sum()

    # Obtener los jugadores únicos
    jugadores = dataframe_total.index

    # Orden deseado de los jugadores
    orden = ['[Vpr]-Sicario', 'cheliRp', 'Kaleroth']

    # Reordenar el dataframe según el orden deseado
    dataframe_total = dataframe_total.reindex(orden)

    # Crear la figura y los ejes
    fig, ax = plt.subplots()

    # Definir el ancho de las barras
    bar_width = 0.2

    # Definir las posiciones de las barras
    r1 = np.arange(len(jugadores))
    r2 = [x + bar_width for x in r1]
    r3 = [x + bar_width for x in r2]

    # Graficar las barras para cada columna
    ax.bar(r1, dataframe_total['Eliminacion'], width=bar_width, label='Eliminaciones')
    ax.bar(r2, dataframe_total['ASISTENCIA'], width=bar_width, label='Asistencias')
    ax.bar(r3, dataframe_total['KILLS'], width=bar_width, label='Ko')

    # Etiquetas del eje X
    ax.set_xticks([r + bar_width for r in range(len(jugadores))])
    ax.set_xticklabels(orden)

    # Etiquetas de los ejes
    ax.set_xlabel('Jugador')
    ax.set_ylabel('Total')

    # Título del gráfico
    ax.set_title('Distribución del total por jugador')

    # Leyenda
    ax.legend()

    # Mostrar el gráfico
    plt.show()





def Promedios_tabla(dataframe_mean):
        dataframe_mean = dataframe_mean.iloc[:, :8]
        
        dataframe_mean.columns = ["null", "null2", "Eliminacion.mean", "Asistencias.mean", "KO.mean", "Daño.mean", "tiempo","dia"]

        dataframe_filtered = dataframe_mean.iloc[:, [ 2, 3, 4, 5, 7]].copy()
        dataframe_filtered.columns = [ "Eliminacion.mean", "Asistencias.mean", "KO.mean", "Daño.mean", "dia"]

        return dataframe_filtered
# Imprimir el nuevo DataFrame
#print(dataframe_filtered)
#print(dataframe_mean)

print(Promedios_tabla(dataframe_mean))
Grafico_barras(dataframe)




    