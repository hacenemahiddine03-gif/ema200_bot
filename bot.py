import time
import threading
from flask import Flask
import requests

BOT_TOKEN = "8689273495:AAEBiA59NDYK-GGJpIQiakSQjCnWaBXdTRk"
CHAT_ID = "6420044567"

# 📩 دالة إرسال رسالة
def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": text}
    requests.post(url, data=data)

# 🔁 البوت يخدم دايما
def bot_loop():
    while True:
        send_message("🔥 BOT PRO MAX WORKING 🔥")
        time.sleep(60)  # كل دقيقة

# 🌐 Flask (باش Render ما يطفاهش)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running"

def run_web():
    app.run(host='0.0.0.0', port=10000)

# تشغيل الاثنين مع بعض
threading.Thread(target=run_web).start()
threading.Thread(target=bot_loop).start()
