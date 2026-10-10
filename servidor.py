from flask import Flask, request, jsonify, session
import os
import secrets
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
# En desarrollo local se genera una clave segura si no se configuró una variable
# de entorno. Para conservar sesiones entre reinicios, configurar FLASK_SECRET_KEY.
app.secret_key = os.environ.get("FLASK_SECRET_KEY") or secrets.token_hex(32)

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

def obtener_credenciales():
    """Valida el JSON recibido y devuelve usuario y contraseña, o un error HTTP."""
    if not request.is_json:
        return None, (jsonify({"error": "El cuerpo debe enviarse como JSON"}), 400)

    datos = request.get_json(silent=True)

    if not isinstance(datos, dict):
        return None, (jsonify({"error": "El cuerpo debe ser un objeto JSON válido"}), 400)

    usuario = datos.get("usuario")
    contraseña = datos.get("contraseña")

    if not isinstance(usuario, str) or not usuario.strip():
        return None, (jsonify({"error": "El campo 'usuario' es obligatorio y debe ser texto"}), 400)

    if not isinstance(contraseña, str) or not contraseña.strip():
        return None, (jsonify({"error": "El campo 'contraseña' es obligatorio y debe ser texto"}), 400)

    # Se eliminan espacios al principio y al final del nombre de usuario,
    # pero no de la contraseña, porque forman parte de la credencial.
    return {"usuario": usuario.strip(), "contraseña": contraseña}, None


@app.route("/registro", methods=["POST"])
def registro():

    datos, error = obtener_credenciales()
    if error:
        return error

    usuario = datos["usuario"]
    contraseña = datos["contraseña"]

    contraseña_hasheada = generate_password_hash(contraseña)

    conexion = None
    try:
        conexion = sqlite3.connect("usuarios.db")
        cursor = conexion.cursor()

        cursor.execute(
            "INSERT INTO usuarios (usuario, contraseña) VALUES (?, ?)",
            (usuario, contraseña_hasheada)
        )

        conexion.commit()
        return jsonify({"mensaje": "Usuario registrado correctamente"}), 201

    except sqlite3.IntegrityError:
        if conexion is not None:
            conexion.rollback()
        return jsonify({"error": "El usuario ya existe"}), 409

    finally:
        if conexion is not None:
            conexion.close()

@app.route("/login", methods=["POST"])
def login():

    datos, error = obtener_credenciales()
    if error:
        return error

    usuario = datos["usuario"]
    contraseña = datos["contraseña"]

    conexion = sqlite3.connect("usuarios.db")
    try:
        cursor = conexion.cursor()

        cursor.execute(
            "SELECT contraseña FROM usuarios WHERE usuario = ?",
            (usuario,)
        )

        resultado = cursor.fetchone()
    finally:
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
    app.run()