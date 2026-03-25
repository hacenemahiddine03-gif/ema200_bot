import time
import requests
from threading import Thread

TOKEN = "8689273495:AAEBiA59NDYK-GGJpIQiakSQjCnWaBXdTRk"
CHAT_ID = "6420044567"

def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.get(url, params={"chat_id": CHAT_ID, "text": text})

def run_flask():
    from flask import Flask
    app = Flask(__name__)

    @app.route('/')
    def home():
        return "Bot running"

    app.run(host='0.0.0.0', port=10000)

def bot_loop():
    last_alive = time.time()

    while True:
        try:
            # هنا تحط الكود تاع الاستراتيجية

            # ⏰ رسالة كل ساعة
            if time.time() - last_alive > 3600:
                send_message("🟢 Bot Alive")
                last_alive = time.time()

            time.sleep(60)

        except Exception as e:
            print("Error:", e)
            time.sleep(10)

if __name__ == "__main__":
    t1 = Thread(target=run_flask)
    t1.start()

    send_message("🔥 BOT STARTED 🔥")

    bot_loop()
