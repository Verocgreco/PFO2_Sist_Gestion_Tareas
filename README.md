# PFO 2 — Sistema de Gestión de Tareas con API y Base de Datos

**Materia:** Programación sobre Redes  
**Objetivo:** desarrollar una API con Flask, persistencia en SQLite, registro e inicio de sesión, y un recurso protegido.

## Descripción

El proyecto permite registrar usuarios, almacenar sus contraseñas mediante hashing, iniciar sesión y acceder al endpoint protegido `GET /tareas`. Este endpoint devuelve una página HTML de bienvenida cuando existe una sesión iniciada.

El proyecto incluye un cliente de consola en Python para interactuar con la API y una página estática (`index.html`) publicada en GitHub Pages.

## Tecnologías

- Python 3
- Flask
- SQLite (`sqlite3`)
- Werkzeug para generar y verificar hashes de contraseñas
- Requests para el cliente de consola
- Thunder Client para probar los endpoints
- GitHub y GitHub Pages

## Estructura del proyecto

```text
PFO2/
├── servidor.py   # API Flask, autenticación y conexión con SQLite
├── cliente.py    # Cliente de consola
├── index.html    # Página estática publicada en GitHub Pages
└── README.md     # Documentación
```

El archivo `usuarios.db` se crea automáticamente al ejecutar `servidor.py`. Los usuarios registrados se guardan allí de forma persistente.

## Requisitos e instalación

Se necesita Python 3 instalado. Desde una terminal abierta en la carpeta del proyecto, instalar las dependencias con:

```bash
python -m pip install flask requests
```

Werkzeug se instala como dependencia de Flask.

## Cómo ejecutar el proyecto

### 1. Iniciar el servidor

En una terminal, ejecutar:

```bash
python servidor.py
```

El servidor local estará disponible en `http://127.0.0.1:5000`. Mantener esta terminal abierta mientras se realizan las pruebas.

La base de datos `usuarios.db` se crea automáticamente si todavía no existe.

La aplicación genera una clave secreta aleatoria para las sesiones si no se define la variable de entorno `FLASK_SECRET_KEY`. En ese caso, al reiniciar el servidor las sesiones anteriores dejan de ser válidas y hay que iniciar sesión nuevamente. Para conservar la clave entre reinicios, se puede configurar esa variable de entorno antes de ejecutar Flask.

### 2. Probar con el cliente de consola

Con el servidor en ejecución, abrir una segunda terminal en la carpeta del proyecto y ejecutar:

```bash
python cliente.py
```

El menú permite:

1. Registrar usuario.
2. Iniciar sesión.
3. Consultar `/tareas`.
4. Salir.

El cliente utiliza `requests.Session()` para conservar las cookies de sesión durante su ejecución. También muestra los códigos HTTP y maneja errores de conexión, tiempo de espera y respuestas que no sean JSON.

## Endpoints de la API

Todas las rutas se prueban localmente en `http://127.0.0.1:5000`.

### `POST /registro` — Registrar usuario

Enviar un cuerpo JSON con los campos `usuario` y `contraseña`:

```json
{
  "usuario": "pfo2",
  "contraseña": "1234"
}
```

- `201 Created`: usuario registrado correctamente.
- `400 Bad Request`: cuerpo JSON inválido o campos obligatorios ausentes o incorrectos.
- `409 Conflict`: el nombre de usuario ya existe.

La contraseña se convierte en un hash antes de guardarse en SQLite; no se almacena en texto plano.

### `POST /login` — Iniciar sesión

Enviar un cuerpo JSON con el usuario y la contraseña registrados:

```json
{
  "usuario": "pfo2",
  "contraseña": "1234"
}
```

- `200 OK`: credenciales correctas; se crea una sesión.
- `400 Bad Request`: cuerpo JSON inválido o campos obligatorios ausentes o incorrectos.
- `401 Unauthorized`: usuario o contraseña incorrectos.

### `GET /tareas` — Recurso protegido

- `401 Unauthorized`: si no hay una sesión iniciada.
- `200 OK`: si el usuario inició sesión; devuelve HTML con una página de bienvenida y el nombre del usuario.

El endpoint muestra una página de bienvenida; no implementa operaciones para crear, editar o eliminar tareas, ya que no forman parte del alcance indicado para esta entrega.

## Pruebas realizadas

Se utilizaron Thunder Client y el cliente de consola para comprobar los siguientes escenarios:

- Registro correcto.
- Comprobación en SQLite de que la contraseña se guarda como hash.
- Inicio de sesión correcto e incorrecto.
- Rechazo del acceso a `/tareas` sin iniciar sesión.
- Acceso a /tareas luego de inicio de sesión correcto.

Las capturas de las pruebas y las respuestas conceptuales se presentan en el documento complementario **“PFO 2 — Pruebas de funcionamiento y respuestas conceptuales”**.

## Seguridad de las contraseñas

Se utiliza `generate_password_hash()` de Werkzeug antes de guardar una contraseña y `check_password_hash()` durante el inicio de sesión. Esto permite verificar las credenciales sin almacenar la contraseña original en texto plano.

## GitHub y GitHub Pages

- **Repositorio:** https://github.com/Verocgreco/PFO2_Sist_Gestion_Tareas
- **GitHub Pages:** https://verocgreco.github.io/PFO2_Sist_Gestion_Tareas/

GitHub Pages publica la página estática `index.html`. No ejecuta el servidor Flask ni aloja la base de datos SQLite. La API y el cliente se ejecutan localmente para las pruebas de esta entrega.
