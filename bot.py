import requests
import time
from flask import Flask
from threading import Thread

TOKEN = "8689273495:AAEBiA59NDYK-GGJpIQiakSQjCnWaBXdTRk"
CHAT_ID = "6420044567"

app = Flask(__name__)

def send_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try:
        requests.post(url, json={"chat_id": CHAT_ID, "text": text})
    except:
        pass

@app.route('/')
def home():
    return "Bot is alive"

def run_flask():
    app.run(host='0.0.0.0', port=10000)

def get_top_symbols():
    try:
        url = "https://fapi.binance.com/fapi/v1/ticker/24hr"
        response = requests.get(url)
        data = response.json()

        usdt_pairs = [s for s in data if "USDT" in s["symbol"]]
        sorted_pairs = sorted(usdt_pairs, key=lambda x: float(x["quoteVolume"]), reverse=True)

        return [s["symbol"] for s in sorted_pairs[:20]]
    except:
        return []

def get_klines(symbol):
    url = f"https://fapi.binance.com/fapi/v1/klines?symbol={symbol}&interval=5m&limit=210"
    data = requests.get(url).json()
    closes = [float(k[4]) for k in data]
    return closes

def ema(data, period=200):
    k = 2 / (period + 1)
    ema_value = data[0]
    for price in data:
        ema_value = price * k + ema_value * (1 - k)
    return ema_value

def check_signal():
    symbols = get_top_symbols()

    for symbol in symbols:
        closes = get_klines(symbol)
        if len(closes) < 200:
            continue

        ema200 = ema(closes)
        price = closes[-1]

        if price > ema200 * 1.01:
            if abs(price - ema200) / ema200 < 0.003:
                send_message(f"🔥 {symbol} NEAR EMA200 AFTER BREAKOUT")

def bot_loop():
    send_message("🔥 BOT STARTED 🔥")

    last_alive = time.time()

    while True:
        try:
            check_signal()

            if time.time() - last_alive > 3600:
                send_message("🟢 Bot Alive")
                last_alive = time.time()

            time.sleep(60)
        except:
            time.sleep(10)

if __name__ == "__main__":
    t1 = Thread(target=run_flask)
    t1.start()

    bot_loop()
