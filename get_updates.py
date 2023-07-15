import requests
import time

def get_updates(token, offset=None):
    # definimos url
    url = f"https://api.telegram.org/bot{token}/getUpdates"
    # asignamos params desde offset
    params = {"offset": offset} if offset else {}
    # obtenemos la respuesta http GET
    response = requests.get(url,params =params)
    # devolvemos en un JSON
    return response.json()

def print_new_messages(token):
    # el siguiente por default no existe
    offset = None
    # Para que haga peticiones siempre
    while True:
        # obtenemos respuestas
        updates = get_updates(token,offset)
        # validamos que hayan resultados desde http GET
        if "result" in updates:
            #imprimimos todas las respuestas
            for update in updates["result"]:
                message = update["result"]
                id = message["from"]["id"]
                username = message['from']["first_name"]
                text = message.get("text")
                print(f"Usuario: {username}({id})")
                print(f"Mensaje: {text}")
                print("-"*20)
                # Pasar al siguiente
                offset = update["update_id"]+1 

        time.sleep(1)
token = "TELEGRAM_TOKEN"
print_new_messages(token)