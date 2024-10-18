from flask import Flask, jsonify, render_template, request
from bd import obtener_jugadores, obtener_equipos, obtener_estadisticas
from auth import require_apikey  # Importar el decorador de autenticación

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/jugadores", methods=['GET'])
@require_apikey  
def get_jugadores():
    id_equipo = request.args.get('id_equipo')
    posicion = request.args.get('posicion')
    edad = request.args.get('edad')
    jugadores = obtener_jugadores(id_equipo, posicion, edad)
    return jsonify(jugadores)

@app.route("/equipos", methods=['GET'])
@require_apikey
def get_equipos():
    equipos = obtener_equipos()
    return jsonify(equipos)

@app.route("/estadisticas", methods=['GET'])
@require_apikey 
def get_estadisticas():
    estadisticas = obtener_estadisticas()
    return jsonify(estadisticas)

if __name__ == "__main__":
    app.run(host='localhost', port=5001, debug=True)
