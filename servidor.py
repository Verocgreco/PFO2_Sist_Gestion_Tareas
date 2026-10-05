from flask import Flask, request, jsonify, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "clave-secreta-pfo2"

def crear_base_datos():
    conexion = sqlite3.connect("usuarios.db")

    cursor = conexion.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            contraseña TEXT NOT NULL
        )
    """)

    conexion.commit()
    conexion.close()

@app.route("/registro", methods=["POST"])
def registro():

    datos = request.get_json()

    usuario = datos.get("usuario")
    contraseña = datos.get("contraseña")

    if not usuario or not contraseña:
        return jsonify({"error": "Faltan datos"}), 400

    contraseña_hasheada = generate_password_hash(contraseña)

    try:
        conexion = sqlite3.connect("usuarios.db")
        cursor = conexion.cursor()

        cursor.execute(
            "INSERT INTO usuarios (usuario, contraseña) VALUES (?, ?)",
            (usuario, contraseña_hasheada)
        )

        conexion.commit()
        conexion.close()

        return jsonify({"mensaje": "Usuario registrado correctamente"}), 201

    except sqlite3.IntegrityError:
        return jsonify({"error": "El usuario ya existe"}), 409

@app.route("/login", methods=["POST"])
def login():

    datos = request.get_json()

    usuario = datos.get("usuario")
    contraseña = datos.get("contraseña")

    conexion = sqlite3.connect("usuarios.db")
    cursor = conexion.cursor()

    cursor.execute(
        "SELECT contraseña FROM usuarios WHERE usuario = ?",
        (usuario,)
    )

    resultado = cursor.fetchone()

    conexion.close()

    if resultado is None:
        return jsonify({"error": "Usuario o contraseña incorrectos"}), 401

    contraseña_hasheada = resultado[0]

    if check_password_hash(contraseña_hasheada, contraseña):
        session["usuario"] = usuario
        return jsonify({"mensaje": "Inicio de sesión exitoso"}), 200

    return jsonify({"error": "Usuario o contraseña incorrectos"}), 401

@app.route("/tareas", methods=["GET"])
def tareas():

    if "usuario" not in session:
        return jsonify({"error": "Debe iniciar sesión para acceder a las tareas"}), 401

    usuario = session["usuario"]

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Tareas</title>
    </head>
    <body>
        <h1>Bienvenido al sistema de gestión de tareas</h1>
        <p>Usuario: {usuario}</p>
        <p>Has accedido correctamente al sistema.</p>
    </body>
    </html>
    """

if __name__ == "__main__":
    crear_base_datos()
    app.run(debug=True)