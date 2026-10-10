import requests

URL = "http://127.0.0.1:5000"
TIEMPO_ESPERA = 5

sesion = requests.Session()


def mostrar_respuesta(respuesta):
    """Muestra el estado HTTP y el contenido de la respuesta del servidor."""
    print(f"\nCódigo HTTP: {respuesta.status_code}")
    print("Respuesta del servidor:")

    try:
        print(respuesta.json())
    except requests.exceptions.JSONDecodeError:
        # Algunas respuestas, como /tareas, contienen HTML en lugar de JSON.
        print(respuesta.text)


def realizar_solicitud(metodo, ruta, **kwargs):
    """Realiza una solicitud HTTP y maneja errores de conexión y tiempo."""
    try:
        respuesta = sesion.request(
            metodo,
            f"{URL}{ruta}",
            timeout=TIEMPO_ESPERA,
            **kwargs
        )
        mostrar_respuesta(respuesta)
        return respuesta
    except requests.exceptions.Timeout:
        print("Error: el servidor tardó demasiado en responder.")
    except requests.exceptions.ConnectionError:
        print("Error: no se pudo conectar con el servidor. Verifique que Flask esté ejecutándose.")
    except requests.exceptions.RequestException as error:
        print(f"Error al realizar la solicitud: {error}")

    return None


def registrar_usuario():
    usuario = input("Ingrese usuario: ")
    contraseña = input("Ingrese contraseña: ")
    realizar_solicitud(
        "POST",
        "/registro",
        json={"usuario": usuario, "contraseña": contraseña}
    )


def iniciar_sesion():
    usuario = input("Ingrese usuario: ")
    contraseña = input("Ingrese contraseña: ")
    realizar_solicitud(
        "POST",
        "/login",
        json={"usuario": usuario, "contraseña": contraseña}
    )


def ver_tareas():
    realizar_solicitud("GET", "/tareas")


def menu():
    while True:
        print("\n==============================")
        print("   CLIENTE DE LA API")
        print("==============================")
        print("1. Registrar usuario")
        print("2. Iniciar sesión")
        print("3. Ver tareas")
        print("4. Salir")

        opcion = input("\nSeleccione una opción: ")

        if opcion == "1":
            registrar_usuario()
        elif opcion == "2":
            iniciar_sesion()
        elif opcion == "3":
            ver_tareas()
        elif opcion == "4":
            print("Programa finalizado.")
            break
        else:
            print("Opción no válida.")


if __name__ == "__main__":
    menu()
