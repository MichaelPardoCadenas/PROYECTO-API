import mysql.connector


def crear_conexion():
        return mysql.connector.connect(
                user='root',
                password='',
                host='127.0.0.1',
                port=3306,
                database='proyecto_nba'
        )


def obtener_jugadores(id_equipo=None):
        connection = crear_conexion()
        cursor = connection.cursor(dictionary=True)

        if id_equipo:
                cursor.execute("SELECT nombre, id_equipo, edad, posicion FROM jugadores WHERE id_equipo = %s", (id_equipo,))
        else:
                cursor.execute("SELECT nombre, id_equipo, edad, posicion FROM jugadores")

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
