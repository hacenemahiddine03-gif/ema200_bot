import requests
import time

BOT_TOKEN = "YOUR_TOKEN"
CHAT_ID = "YOUR_CHAT_ID"

symbols = [
"ARBUSDT","NEOUSDT","MORPHOUSDT","JTOUSDT","CFXUSDT","IMXUSDT",
"INJUSDT","TIAUSDT","PENDLEUSDT","CHZUSDT","SEIUSDT","XTZUSDT",
"STXUSDT","CAKEUSDT","OPUSDT","ETHFIUSDT","FETUSDT","VETUSDT",
"JUPUSDT","ENSUSDT","ALGOUSDT","ENAUSDT","APTUSDT","QNTUSDT",
"RENDERUSDT","ATOMUSDT","FILUSDT","ZROUSDT"
]

last_signal = {}

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})

def get_klines(symbol):
    url = f"https://fapi.binance.com/fapi/v1/klines?symbol={symbol}&interval=1m&limit=210"
    return requests.get(url).json()

def ema(prices, period=200):
    k = 2 / (period + 1)
    ema_val = prices[0]
    for price in prices:
        ema_val = price * k + ema_val * (1 - k)
    return ema_val

def rsi(prices, period=14):
    gains, losses = 0, 0
    for i in range(1, period+1):
        diff = prices[-i] - prices[-i-1]
        if diff > 0:
            gains += diff
        else:
            losses -= diff
    if losses == 0:
        return 100
    rs = gains / losses
    return 100 - (100 / (1 + rs))

def is_bearish_engulfing(c):
    return float(c[-2][4]) > float(c[-2][1]) and float(c[-1][4]) < float(c[-1][1]) and float(c[-1][4]) < float(c[-2][1])

def is_bullish_engulfing(c):
    return float(c[-2][4]) < float(c[-2][1]) and float(c[-1][4]) > float(c[-1][1]) and float(c[-1][4]) > float(c[-2][1])

def check_symbol(symbol):
    try:
        data = get_klines(symbol)

        closes = [float(c[4]) for c in data]
        volumes = [float(c[5]) for c in data]

        ema200 = ema(closes)
        rsi_val = rsi(closes)

        price = closes[-1]
        prev_price = closes[-2]

        volume_now = volumes[-1]
        volume_avg = sum(volumes[-20:]) / 20

        near_ema = abs(price - ema200) / ema200 < 0.002
        high_volume = volume_now > volume_avg * 1.5

        # 🔻 SHORT
        if (price < ema200 and near_ema and
            is_bearish_engulfing(data) and
            rsi_val > 60 and high_volume):

            if last_signal.get(symbol) != "short":
                send_telegram(f"🔻 SHORT {symbol}\nEMA Reject + Volume\nRSI: {round(rsi_val,1)}")
                last_signal[symbol] = "short"

        # 🔺 LONG
        elif (price > ema200 and near_ema and
              is_bullish_engulfing(data) and
              rsi_val < 40 and high_volume):

            if last_signal.get(symbol) != "long":
                send_telegram(f"🔺 LONG {symbol}\nEMA Bounce + Volume\nRSI: {round(rsi_val,1)}")
                last_signal[symbol] = "long"

    except:
        pass

send_telegram("🔥 BOT PRO MAX STARTED 🔥")

while True:
    for s in symbols:
        check_symbol(s)
        time.sleep(0.5)
