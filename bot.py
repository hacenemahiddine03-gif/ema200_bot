import time
import threading
import os
from flask import Flask
import requests

BOT_TOKEN = "8689273495:AAEBiA59NDYK-GGJpIQiakSQjCnWaBXdTRk"
CHAT_ID = "6420044567"

# 📩 إرسال رسالة
def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": text})

# 🔁 البوت يخدم باستمرار
def bot_loop():
    while True:
        print("Bot is running...")
        send_message("✅ Bot is working")
        time.sleep(60)

# 🌐 Flask (باش Render ما يطفاهش)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive"

def run_web():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))

# ▶️ تشغيل الاثنين
if __name__ == "__main__":
    threading.Thread(target=run_web).start()
    threading.Thread(target=bot_loop).start()
