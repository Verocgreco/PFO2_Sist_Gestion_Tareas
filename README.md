# PFO 2 — Sistema de Gestión de Tareas con API y Base de Datos

## Descripción

Este proyecto consiste en el desarrollo de una API REST utilizando Flask, con persistencia de datos mediante SQLite y un sistema básico de autenticación de usuarios.

La aplicación permite registrar usuarios, almacenar sus contraseñas de forma segura mediante hashing, iniciar sesión mediante la verificación de credenciales y acceder a un recurso protegido de tareas.

El proyecto fue desarrollado como parte de la PFO 2 de la materia **Programación sobre Redes**.

---

## Tecnologías utilizadas

- **Python**
- **Flask** — desarrollo de la API REST.
- **SQLite** — almacenamiento persistente de los usuarios.
- **Werkzeug** — hashing y verificación segura de contraseñas.
- **Thunder Client** — pruebas de los endpoints.
- **GitHub** — repositorio y documentación del proyecto.

---

## Estructura del proyecto

```text
PFO2/
│
├── servidor.py
├── usuarios.db
└── README.md
```

### Archivos principales

- `servidor.py`: contiene la API Flask, los endpoints, la conexión con SQLite y el sistema de autenticación.
- `usuarios.db`: base de datos SQLite generada automáticamente al ejecutar el servidor.
- `README.md`: documentación del proyecto.

---

## Requisitos

Para ejecutar el proyecto se necesita:

- Python 3 instalado.
- Flask.
- Un cliente para realizar pruebas de API, como Thunder Client.

### Instalación de Flask

Desde la terminal, dentro de la carpeta del proyecto:

```bash
pip install flask
```

La librería Werkzeug se instala automáticamente como dependencia de Flask.

---

## Ejecución

Ubicarse mediante la terminal en la carpeta del proyecto y ejecutar:

```bash
python servidor.py
```

Si el servidor se inicia correctamente, Flask mostrará una dirección similar a:

```text
http://127.0.0.1:5000
```

La base de datos `usuarios.db` se crea automáticamente al iniciar el servidor.

---

# Endpoints de la API

## 1. Registro de usuarios

### POST `/registro`

Permite registrar un nuevo usuario.

**URL:**

```text
http://127.0.0.1:5000/registro
```

**Body JSON:**

```json
{
    "usuario": "pfo2",
    "contraseña": "1234"
}
```

La contraseña recibida no se almacena directamente. Antes de guardarla en SQLite se genera un hash mediante Werkzeug.

### Respuesta exitosa

```json
{
    "mensaje": "Usuario registrado correctamente"
}
```

Código HTTP:

```text
201 Created
```

Si el usuario ya existe, la API devuelve:

```json
{
    "error": "El usuario ya existe"
}
```

---

## 2. Inicio de sesión

### POST `/login`

Permite verificar las credenciales de un usuario registrado.

**URL:**

```text
http://127.0.0.1:5000/login
```

**Body JSON:**

```json
{
    "usuario": "pfo2",
    "contraseña": "1234"
}
```

Si las credenciales son correctas, se crea una sesión para el usuario.

### Respuesta exitosa

```json
{
    "mensaje": "Inicio de sesión exitoso"
}
```

Código HTTP:

```text
200 OK
```

### Credenciales incorrectas

Si el usuario o la contraseña no son correctos:

```json
{
    "error": "Usuario o contraseña incorrectos"
}
```

Código HTTP:

```text
401 Unauthorized
```

---

## 3. Acceso a las tareas

### GET `/tareas`

Este endpoint está protegido y solamente permite el acceso a usuarios que hayan iniciado sesión correctamente.

**URL:**

```text
http://127.0.0.1:5000/tareas
```

### Sin autenticación

Si se intenta acceder sin iniciar sesión:

```json
{
    "error": "Debe iniciar sesión para acceder a las tareas"
}
```

Código HTTP:

```text
401 Unauthorized
```

### Con autenticación

Luego de iniciar sesión correctamente, el endpoint devuelve una página HTML de bienvenida:

```text
Bienvenido al sistema de gestión de tareas

Usuario: pfo2

Has accedido correctamente al sistema.
```

---

# Pruebas realizadas

Se realizaron pruebas utilizando Thunder Client para verificar el correcto funcionamiento de la API.

### Registro exitoso

Se verificó que un usuario pueda registrarse correctamente y que la contraseña sea almacenada mediante un hash en SQLite.

**Resultado:** `201 Created`

### Acceso sin autenticación

Se intentó acceder a `/tareas` sin haber iniciado sesión.

**Resultado:** `401 Unauthorized`

### Inicio de sesión exitoso

Se utilizaron credenciales válidas para comprobar el inicio de sesión.

**Resultado:** `200 OK`

### Inicio de sesión fallido

Se utilizaron credenciales incorrectas para comprobar el rechazo de acceso.

**Resultado:** `401 Unauthorized`

### Acceso autenticado

Luego de iniciar sesión correctamente se accedió nuevamente a `/tareas`.

**Resultado:** página HTML de bienvenida.

---

# Seguridad de las contraseñas

Las contraseñas no se almacenan en texto plano.

Para protegerlas se utiliza la función `generate_password_hash()` de Werkzeug, que genera un hash de la contraseña antes de almacenarlo en SQLite.

Para verificar una contraseña durante el inicio de sesión se utiliza `check_password_hash()`.

De esta manera, aunque alguien pudiera acceder a la base de datos, no encontraría las contraseñas originales almacenadas directamente.

---

# Repositorio

El código fuente del proyecto se encuentra disponible en el repositorio de GitHub correspondiente a la PFO 2.