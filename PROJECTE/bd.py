import mysql.connector


def crear_conexion():
        return mysql.connector.connect(
                user='root',
                password='',
                host='127.0.0.1',
                port=3306,
                database='proyecto_nba'
        )


def obtener_jugadores(id_equipo=None, posicion=None, edad=None):
        connection = crear_conexion()
        cursor = connection.cursor(dictionary=True)

        query = "SELECT nombre, id_equipo, edad, posicion FROM jugadores WHERE 1=1"
        params = []

        if id_equipo:
                query += " AND id_equipo = %s"
                params.append(id_equipo)

        if posicion:
                query += " AND posicion = %s"
                params.append(posicion)
        
        if edad:
                query += " AND edad = %s"
                params.append(edad)

        cursor.execute(query, tuple(params))
        data = cursor.fetchall()
        cursor.close()
        connection.close()
        return data



def obtener_equipos():
        connection = crear_conexion()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM equipos")
        data = cursor.fetchall()
        cursor.close()
        connection.close()
        return data


def obtener_estadisticas():
        connection = crear_conexion()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM estadisticas")
        data = cursor.fetchall()
        cursor.close()
        connection.close()
        return data
