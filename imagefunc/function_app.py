import os
import logging
import azure.functions as func
from openai import OpenAI

# Llave secreta para la API de OpenAI
secret_key = os.getenv("OPENAI_API_KEY")

# Inicializa el cliente de OpenAI
client = OpenAI(api_key=secret_key)

def main(req: func.HttpRequest) -> func.HttpResponse:
    """Punto de entrada para la función imagefunc."""
    logging.info('Python HTTP trigger function processed a request.')

    try:
        # Obtener el cuerpo de la solicitud como JSON
        req_body = req.get_json()

        # Llamar a la API de OpenAI para generar una imagen con DALL-E
        completion = client.images.generate(
            model="dall-e-3",
            prompt=req_body["prompt"],
            n=1,
            size="1024x1024"
        )

        # Retornar la URL de la imagen generada
        return func.HttpResponse(
            completion.data[0].url,
            status_code=200
        )

    except Exception as e:
        # Manejar errores y registrar la excepción
        logging.error(f"Error processing request: {str(e)}")
        return func.HttpResponse(
            f"An error occurred: {str(e)}",
            status_code=500
        )