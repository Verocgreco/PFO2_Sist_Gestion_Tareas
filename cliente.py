import requests

URL = "http://127.0.0.1:5000"

sesion = requests.Session()


def registrar_usuario():
    usuario = input("Ingrese usuario: ")
    contraseña = input("Ingrese contraseña: ")

    respuesta = sesion.post(
        f"{URL}/registro",
        json={
            "usuario": usuario,
            "contraseña": contraseña
        }
    )

    print("\nRespuesta del servidor:")
    print(respuesta.json())


def iniciar_sesion():
    usuario = input("Ingrese usuario: ")
    contraseña = input("Ingrese contraseña: ")

    respuesta = sesion.post(
        f"{URL}/login",
        json={
            "usuario": usuario,
            "contraseña": contraseña
        }
    )

    print("\nRespuesta del servidor:")
    print(respuesta.json())


def ver_tareas():
    respuesta = sesion.get(f"{URL}/tareas")

    print("\nRespuesta del servidor:")
    print(respuesta.text)


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