import mysql.connector

## ---------------------------------------    DATOS MODIFICABLES
##----------------------------------------   MODIFIABLE DATA



base = mysql.connector.connect(
          user="root",
          password="KEnny12345626482",
          host="localhost"
)





#CREA LA BASE DE DATOS, IMPORTANTE SI MODIFICAS EL NOMBRE DE LA BASE DE DATOS HAY QUE PONER EL MOISMO NOMBRE EN EL RESTO DE LOS SCRIPTS
#CREATE THE DATABASE, IMPORTANT IF YOU MODIFY THE NAME OF THE DATABASE YOU MUST PUT THE SAME NAME IN THE REST OF THE SCRIPTS

cursor = base.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS PRUEBAS_BORRAR")    #PRUEBAS_BORRAR
cursor.execute("USE PRUEBAS_BORRAR")



###------------------------------------------------------------------    CREANDO LAS TABLAS

create_tables_query = """
CREATE TABLE IF NOT EXISTS Mapas(
    id_map INT NOT NULL AUTO_INCREMENT,
    Mapa VARCHAR(255) NOT NULL,
    Hora_inicio TIME NOT NULL,
    Hora_fin TIME NOT NULL,
    Fecha_mapa DATE,
    PRIMARY KEY (id_map)
);
"""

cursor.execute(create_tables_query)

create_tables_query = """
CREATE TABLE IF NOT EXISTS Jugador(
    PID INT AUTO_INCREMENT NOT NULL,
    Nombre VARCHAR(16),
    PRIMARY KEY (PID)
);
"""

cursor.execute(create_tables_query)

create_tables_query = """
CREATE TABLE IF NOT EXISTS Partidas(
    MatchID INT AUTO_INCREMENT,
    Fecha DATE NOT NULL,
    hora TIME,
    PID1 INT,
    PID2 INT,
    PID3 INT,
    Posicion_Peloton INT,
    Ruta_Imagen VARCHAR(200),
    Dia_Numero INT,
    PRIMARY KEY (MatchID),
    FOREIGN KEY (PID1) REFERENCES Jugador(PID),
    FOREIGN KEY (PID2) REFERENCES Jugador(PID),
    FOREIGN KEY (PID3) REFERENCES Jugador(PID)
);
"""

cursor.execute(create_tables_query)

create_tables_query = """
CREATE TABLE IF NOT EXISTS Resultados_Partida(
    ID INT NOT NULL AUTO_INCREMENT,
    MatchID INT NOT NULL,
    PlayerID INT NOT NULL,
    Eliminacion INT,
    Asistencia INT,
    kills INT,
    Daño INT,
    tiempo TIME,
    Error_DATOS INT,
    PRIMARY KEY (ID),
    FOREIGN KEY (MatchID) REFERENCES Partidas(MatchID)
);
"""

cursor.execute(create_tables_query)



#-------------------------------------------------------------------  FIN DE CREAR TABLAS

##  -----------------------------------------------------------------------------CREAMOS LOS TRIGGERS


create_triggers_query = """
CREATE TRIGGER Fechass
BEFORE INSERT ON Partidas
FOR EACH ROW 
BEGIN
    DECLARE DIFERENCIA_HORAS INT;
    DECLARE Fecha_Anterior DATE;
    DECLARE Hora_Anterior TIME;
    DECLARE Dia_Numero_aTRAS INT;
    DECLARE DIF_DIAS INT;

    IF NEW.Fecha IS NULL THEN
        SET NEW.Fecha = CURRENT_DATE();
    END IF;

    IF NEW.hora IS NULL THEN
        SET NEW.hora = CURRENT_TIME();
    END IF;

    SELECT Fecha, hora, Dia_Numero
    INTO Fecha_Anterior, Hora_Anterior, Dia_Numero_aTRAS
    FROM Partidas
    WHERE MatchID =(SELECT MAX(MATchid) FROM Partidas);

    SET DIFERENCIA_HORAS = TIMESTAMPDIFF(HOUR, Hora_Anterior, NEW.hora);

    SET DIF_DIAS = TIMESTAMPDIFF(DAY, Fecha_Anterior, NEW.FECHA);

    IF DIF_DIAS > 1 THEN
        SET NEW.Dia_Numero = Dia_Numero_aTRAS + 1;
    ELSE 
        IF DIFERENCIA_HORAS > 1 THEN
            SET NEW.Dia_Numero = Dia_Numero_aTRAS + 1;	
        ELSE
            SET NEW.Dia_Numero = Dia_Numero_aTRAS;
        END IF;
    END IF;

    IF DIFERENCIA_HORAS IS NULL THEN
        SET NEW.Dia_Numero = 1;
    END IF;
END;
"""
try:
    cursor.execute(create_triggers_query)
except Exception as e:
    print(e)
create_triggers_query = """
CREATE TRIGGER MALOS_vALORES
BEFORE INSERT ON Resultados_Partida
FOR EACH ROW
BEGIN
    DECLARE Numero_insertar INT;
    SET Numero_insertar = 0;

    IF NEW.Eliminacion = 99 THEN
        SET NEW.Eliminacion = NULL;
        SET Numero_insertar = 1;
    END IF;

    IF NEW.Asistencia = 99 THEN
        SET NEW.Asistencia = NULL;
        SET Numero_insertar = CONCAT(Numero_insertar, 2);
    END IF;

    IF NEW.kills = 99 THEN
        SET NEW.kills = NULL;
        SET Numero_insertar = CONCAT(Numero_insertar, 3);
    END IF;

    IF NEW.Daño = 9999 THEN
        SET NEW.Daño = NULL;
        SET Numero_insertar = CONCAT(Numero_insertar, 4);
    END IF;

    IF NEW.tiempo = '00:59:59' THEN
        SET NEW.tiempo = NULL;
        SET Numero_insertar = CONCAT(Numero_insertar, 5);
    END IF;

    IF Numero_insertar != 0 THEN
        SET NEW.Error_DATOS = Numero_insertar;
    END IF;
END;
"""

try:
    cursor.execute(create_triggers_query)
except Exception as e:
    print(e)
create_triggers_query =  """
CREATE TRIGGER Correccion_datos
BEFORE UPDATE ON Resultados_Partida
FOR EACH ROW
BEGIN
    IF NEW.Eliminacion IS NOT NULL AND NEW.Asistencia IS NOT NULL AND NEW.kills IS NOT NULL AND NEW.daño IS NOT NULL AND NEW.tiempo IS NOT NULL
    THEN SET NEW.error_datos = NULL;
    END IF;

    IF NEW.Eliminacion IS  NULL OR NEW.Asistencia IS  NULL OR NEW.kills IS  NULL OR NEW.daño IS NULL OR NEW.tiempo IS  NULL
    THEN SET 
            NEW.error_datos = 6;
    END IF;
END;
"""

try:
    cursor.execute(create_triggers_query)
except Exception as e:
    print(e)
create_triggers_query ="""
CREATE TRIGGER PONE_FECHAS
BEFORE INSERT ON Mapas
FOR EACH ROW
BEGIN
    IF NEW.Fecha_MAPA IS NULL THEN
        SET NEW.Fecha_MAPA = CURRENT_DATE();
    END IF;
END;
"""

try:
    cursor.execute(create_triggers_query)
except Exception as e:
    print(e)

##  ---------------------------------------------------------------------------- CREA  EL VIEW
try:
    cursor.execute(create_triggers_query)
except Exception as e:
    print(e)
create_triggers_query ="""
CREATE VIEW Tabla_definitiva AS

SELECT   
	s.id,
    s.matchid AS MatchID,
    e.nombre as Nombre,
    s.eliminacion as Eliminaciones,
    s.asistencia as Asistencias,
    s.kills as KO,
    s.daño as Daño,
    s.tiempo as Tiempo_Supervivencia,
    x.Posicion_Peloton,
    
    x.fecha as Fecha,
    x.hora as Hora,
    x.Dia_Numero as Dias,
    s.Error_DATOS as Fallo_Valores,
    ee.mapa as Mapa
    
FROM
    Resultados_Partida s
        JOIN
    jugador e ON e.PID = s.PlayerID 
join 
    Partidas x
on

    x.matchid = s.matchid
left join  (SELECT m.mapa,R.HORA ,r.posicion_peloton, r.fecha AS fecha_partidas, m.Fecha_mapa AS Fecha_mapa , r.matchid
FROM Partidas r 
JOIN mapas m ON (r.fecha = m.Fecha_mapa) AND (r.hora BETWEEN m.hora_inicio AND m.hora_fin)) as ee
on ee.matchid=s.matchid    

ORDER BY matchid DESC;
"""

try:
    cursor.execute(create_triggers_query)
except Exception as e:
    print(e)
##--------------------------------------------------------------------- guardamos los cambios realizados 
base.commit()


cursor.close()
base.close()

print("Bases de datos y triggers creados con éxito.")
print("Databases and triggers created successfully.")