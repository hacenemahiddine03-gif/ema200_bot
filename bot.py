import requests
import time

BOT_TOKEN = "8689273495:AAEBiA59NDYK-GGJpIQiakSQjCnWaBXdTRk"
CHAT_ID = "6420044567"

last_signal = {}

def send_telegram(msg):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": CHAT_ID, "text": msg})
    except:
        pass

def get_top_symbols():
    try:
        url = "https://fapi.binance.com/fapi/v1/ticker/24hr"
        data = requests.get(url).json()
        usdt_pairs = [s for s in data if "USDT" in s["symbol"]]
        sorted_pairs = sorted(usdt_pairs, key=lambda x: float(x["quoteVolume"]), reverse=True)
        return [s["symbol"] for s in sorted_pairs[:20]]
    except:
        return []

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

def liquidity_sweep_high(data):
    highs = [float(c[2]) for c in data[-10:-1]]
    return float(data[-1][2]) > max(highs)

def liquidity_sweep_low(data):
    lows = [float(c[3]) for c in data[-10:-1]]
    return float(data[-1][3]) < min(lows)

def check_symbol(symbol):
    try:
        data = get_klines(symbol)

        closes = [float(c[4]) for c in data]
        volumes = [float(c[5]) for c in data]

        ema200 = ema(closes)
        rsi_val = rsi(closes)

        price = closes[-1]

        volume_now = volumes[-1]
        volume_avg = sum(volumes[-20:]) / 20

        near_ema = abs(price - ema200) / ema200 < 0.002
        high_volume = volume_now > volume_avg * 1.5

        sweep_high = liquidity_sweep_high(data)
        sweep_low = liquidity_sweep_low(data)

        if (price < ema200 and near_ema and
            is_bearish_engulfing(data) and
            rsi_val > 60 and high_volume and sweep_high):

            if last_signal.get(symbol) != "short":
                send_telegram(f"🔻 SHORT {symbol}\nEMA + Volume + PA + Sweep\nRSI: {round(rsi_val,1)}")
                last_signal[symbol] = "short"

        elif (price > ema200 and near_ema and
              is_bullish_engulfing(data) and
              rsi_val < 40 and high_volume and sweep_low):

            if last_signal.get(symbol) != "long":
                send_telegram(f"🔺 LONG {symbol}\nEMA + Volume + PA + Sweep\nRSI: {round(rsi_val,1)}")
                last_signal[symbol] = "long"

    except:
        pass

send_telegram("🔥 BOT PRO MAX (LIQUIDITY) STARTED 🔥")

symbols = get_top_symbols()

last_update = time.time()
last_alive = time.time()

while True:
    try:
        now = time.time()

        if now - last_update > 86400:
            symbols = get_top_symbols()
            send_telegram(f"📊 Top 20 updated:\n{symbols}")
            last_update = now

        if now - last_alive > 3600:
            send_telegram("🟢 Bot Alive")
            last_alive = now

        if not symbols:
            symbols = get_top_symbols()

        for s in symbols:
            check_symbol(s)
            time.sleep(0.5)

    except:
        time.sleep(5)
