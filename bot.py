import time
import threading
from flask import Flask
import requests

BOT_TOKEN = "8689273495:AAEBiA59NDYK-GGJpIQiakSQjCnWaBXdTRk"
CHAT_ID = "6420044567"

def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": text})

def bot_loop():
    while True:
        print("Bot is running...")
        send_message("✅ Bot is working")
        time.sleep(60)

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive"

def run_web():
    app.run(host='0.0.0.0', port=10000)

if __name__ == "__main__":
    threading.Thread(target=run_web).start()
    threading.Thread(target=bot_loop).start()
