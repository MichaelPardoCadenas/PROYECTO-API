from functools import wraps
from flask import request, jsonify
import mysql.connector
import bcrypt
import os

def verificar_apikey(apikey_proporcionada):
    connection = mysql.connector.connect(
        user='root',
        password='',
        host='127.0.0.1',
        port=3306,
        database='proyecto_nba'
    )
    cursor = connection.cursor(dictionary=True)

    try:
        # Buscar el hash basado en el id_usuario o cualquier otro identificador adecuado
        query = "SELECT api_key_hash FROM api_keys"
        cursor.execute(query)
        result = cursor.fetchall()

        if result:
            for row in result:
                api_key_hash = row['api_key_hash']

                # Comparar la API key proporcionada con el hash usando bcrypt
                if bcrypt.checkpw(apikey_proporcionada.encode('utf-8'), api_key_hash.encode('utf-8')):
                    print("La API key es válida.")
                    return True

            print("No se encontró una API key válida.")
            return False
        else:
            print("No se encontraron API keys en la base de datos.")
            return False
    except mysql.connector.Error as e:
        print(f"Error al verificar la clave API: {e}")
        return False
    finally:
        cursor.close()
        connection.close()


def require_apikey(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        apikey_proporcionada = request.headers.get('X-API-KEY')
        if not apikey_proporcionada or not verificar_apikey(apikey_proporcionada):
            return jsonify({'message': 'API key no válida o ausente'}), 403
        return f(*args, **kwargs)
    return decorated_function

def generar_apikey():
    return os.urandom(16).hex()

def encriptar_apikey(apikey):
    return bcrypt.hashpw(apikey.encode('utf-8'), bcrypt.gensalt()).decode()

def guardar_apikey_encriptada(id_usuario, apikey_encriptada):
    connection = mysql.connector.connect(
        user='root',
        password='',
        host='127.0.0.1',
        port=3306,
        database='proyecto_nba'
    )
    cursor = connection.cursor()

    try:
        # Insertar el hash de la API key en la base de datos
        query = "INSERT INTO api_keys (id_usuario, api_key_hash) VALUES (%s, %s)"
        cursor.execute(query, (id_usuario, apikey_encriptada))
        connection.commit()
        print("Clave API encriptada guardada correctamente.")
    except mysql.connector.Error as e:
        print(f"Error al guardar la clave API en la base de datos: {e}")
    finally:
        cursor.close()
        connection.close()

def generar_y_guardar_apikey(id_usuario):
    # Generar una nueva API key en texto plano
    apikey = generar_apikey()
    print(f"Clave API generada: {apikey}")

    # Encriptar la API key antes de guardarla
    apikey_encriptada = encriptar_apikey(apikey)

    # Guardar el hash en la base de datos
    guardar_apikey_encriptada(id_usuario, apikey_encriptada)

    # Devolver la API key en texto plano para que el usuario la vea
    return apikey

if __name__ == "__main__":
    nueva_apikey = generar_y_guardar_apikey(1)
    print(f"La clave API para el usuario es: {nueva_apikey}")
