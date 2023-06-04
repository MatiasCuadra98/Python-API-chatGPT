# Importamos modulos necesarios
import os
import openai
import argparse

# Mensaje de sistema que proporciona instrucciones al usuario

MENSAJE_SISTEMA = """Indique de manera clara y precisa la pregunta a realizar."""

# funcion main


def main():
    # mensaje de inicio
    print("Inicio de cliente GPT Shell.")

    # configuramos argumentos
    parser = argparse.ArgumentParser()
    parser.add_argument("prompt", nargs="+", type=str,
                        help="Prompt deseado para chatGPT")

    # analizamos los args de la linea de comando
    args = parser.parse_args()

    # combinamos los args en una sola string
    prompt = " ".join(args.prompt)

    # imprimimos el prompt del usuario
    print(f"Pregunta: {prompt}")

    # historial con el chatgpt
    historial_chat = []

    # llamamos a la funcion preguntar_chatgpt para obtener una respuesta inicial
    preguntar_chatgpt(prompt, historial_chat, MENSAJE_SISTEMA)

    # creamos bucle para recibir y procesar el input del usuario
    input_usuario = input(">_: ")
    while input_usuario != "":

        # obtenemos una respuesta a lo preguntado por el usuario
        preguntar_chatgpt(input_usuario, historial_chat, MENSAJE_SISTEMA)
        input_usuario = input(">_: ")

    # mensaje de finalizacion de sesion
    print("Fin de la sesion.")


# definimos la funcion para hacelre preguntas a chatgpt


def preguntar_chatgpt(prompt: str, historial_chat: list, mensaje_sistema: str):

    # configuramos nuestra clave API de OpenAI que se saca de la pagina oficial de openAI
    openai.api_key = os.getenv("OPENAI_API_KEY")

    # creamos un diccionario con el prompt del usuario
    prompt_usuario = {"rol": "usuario", "contenido": prompt}

    # generamos una respuesta de chatgpt usando el modelo gpt-3.5-turbo
    respuesta_gpt = openai.ChatCompletion.create(
        modelo="gpt-3.5-turbo",

        # mensaje del sistema
        mensaje=[{"rol": "sistema", "contenido": mensaje_sistema},

                 # conversacion previa con el chat
                 *historial_chat,

                 # prompt actual del usuario
                 prompt_usuario],
    )

    # obtenemos el contenido de la respuesta que nos dio chatgpt
    contenido = respuesta_gpt["opciones"][0]["mensaje"]["contenido"]

    # agregamos el nuevo prompt del usuario al historial del chatgpt
    historial_chat.append(prompt_usuario)

    historial_chat.append({"rol": "asistente", "contenido": contenido})

    # imprimimos le contenido de la respuesta en color verde
    print("\033[92m" + contenido + "\033[0m")
    return contenido


if __name__ == "__main__":
    # llamamos a la funcion principal del programa
    main()
