import os
import logging
import azure.functions as func
from openai import OpenAI

# Obtener la API key desde las variables de entorno
secret_key = os.getenv("OPENAI_API_KEY")

if not secret_key:
    logging.error("No se encontró la API key en las variables de entorno")
    raise ValueError("Falta la API key en las variables de entorno")

# Inicializa el cliente de OpenAI
client = OpenAI(api_key=secret_key)

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Processing a request in completionAPI.')

    try:
        # Extrae el cuerpo de la solicitud
        req_body = req.get_json()

        # Llama a la API de OpenAI para completar el chat
        completion = client.chat.completions.create(
            model=req_body["model"],
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": req_body["prompt"]}
            ],
            max_tokens=req_body["max_tokens"],
            temperature=req_body["temperature"]
        )

        # Retorna el contenido del mensaje
        return func.HttpResponse(
            completion.choices[0].message.content,
            status_code=200
        )

    except Exception as e:
        # Registrar el error completo en los logs
        logging.error(f"Error: {str(e)}", exc_info=True)
        return func.HttpResponse(
            f"An error occurred: {str(e)}",
            status_code=500
        )
