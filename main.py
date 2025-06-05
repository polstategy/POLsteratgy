import logging
import telebot
import requests
import time
from datetime import datetime, timedelta

BOT_TOKEN = "YOUR_BOT_TOKEN"
bot = telebot.TeleBot(BOT_TOKEN)
SENT_ALERTS = {}  # ذخیره هشدارهای ارسال‌شده برای جلوگیری از تکرار

def get_gold_data(period="weekly"):
    now = datetime.utcnow()
    if period == "weekly":
        start = now - timedelta(days=7)
    elif period == "monthly":
        start = now - timedelta(days=30)
    elif period == "quarterly":
        start = now - timedelta(days=90)
    elif period == "semiannual":
        start = now - timedelta(days=180)
    else:
        start = now - timedelta(days=7)
    end = now

    url = f"https://api.twelvedata.com/time_series?symbol=XAU/USD&interval=1day&start_date={start.date()}&end_date={end.date()}&apikey=YOUR_API_KEY"
    r = requests.get(url).json()
    candles = r.get("values", [])
    if not candles:
        return None

    highs = [float(c["high"]) for c in candles]
    lows = [float(c["low"]) for c in candles]
    closes = [float(c["close"]) for c in candles]

    H = max(highs)
    L = min(lows)
    C = closes[-1]

    M1 = (H + L) / 2
    M2 = (H + M1) / 2
    M3 = (L + M1) / 2
    M4 = (H + M2) / 2
    M5 = (M2 + M1) / 2
    M6 = (M1 + M3) / 2
    M7 = (M3 + L) / 2
    Z1 = (H + L + C) / 3
    pip = abs(H - M4)

    U = [H + pip * (i + 1) for i in range(30)]
    D = [L - pip * (i + 1) for i in range(30)]

    return {
        "H": H, "L": L, "C": C, "M1": M1, "M2": M2, "M3": M3, "M4": M4,
        "M5": M5, "M6": M6, "M7": M7, "Z1": Z1, "pip": pip, "U": U, "D": D
    }

@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    bot.reply_to(message, "سلام! من ربات تحلیل طلا هستم. اطلاعات کندل هفته قبل و سطوح مقاومتی و حمایتی رو بهت می‌دم.")

def check_alerts():
    data = get_gold_data()
    if not data:
        return

    price = get_current_price()
    levels = [data["M1"], data["M2"], data["M3"], data["M4"], data["M5"], data["M6"], data["M7"], data["Z1"]] + data["U"] + data["D"]
    for level in levels:
        key = f"{round(level, 2)}"
        if abs(price - level) < data["pip"] / 10 and key not in SENT_ALERTS:
            bot.send_message(CHAT_ID, f"قیمت به سطح مهم {round(level, 2)} رسیده است!")
            SENT_ALERTS[key] = True

def get_current_price():
    url = "https://api.twelvedata.com/price?symbol=XAU/USD&apikey=YOUR_API_KEY"
    r = requests.get(url).json()
    return float(r["price"])

if __name__ == "__main__":
    print("ربات در حال اجراست...")
    while True:
        try:
            check_alerts()
            time.sleep(60)
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(60)