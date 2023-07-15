import openai
import requests
import time
from dotenv import dotenv_values

config = dotenv_values(".env")

openai.api_key = config["OPENAI_API_KEY"]
TOKEN = config["TELEGRAM_TOKEN"]

def get_updates(offset):
    url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
    params = {"timeout":100,"offset": offset}
    response = requests.get(url,params=params)
    return response.json()["result"]

def send_messages(chat_id,text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    params = {"chat_id": chat_id,"text":text}
    response = requests.post(url,params=params)
    return response

def get_openai_response(prompt):
    model_engine = "MODEL"
    response = openai.Completion.create(
        engine = model_engine,
        prompt = prompt,
        max_tokens = 200,
        n = 1,
        stop=" END",
        temperature=0.5
    )
    return response.choices[0].text.strip()

def main():
    print('Starting bot..')
    offset = 0
    while True:
        #llamada a nuestra funcion actualizadora
        updates = get_updates(offset)
        if updates:
            for update in updates:
                offset = update['update_id']+1
                chat_id = update["message"]["chat"]["id"]
                user_message = update["message"]["text"]
                print(f"Received message: {user_message}")
                GPT = get_openai_response(user_message)
                send_messages(chat_id, GPT)
        else:
            time.sleep(1)

if __name__ == '__main__':
    main()