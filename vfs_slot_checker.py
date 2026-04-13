import requests
import time
from twilio.rest import Client
from datetime import datetime
import os

# ─────────────────────────────────────────
#  KONFİQURASİYA - Railway Environment Variables-dan oxuyur
# ─────────────────────────────────────────
TWILIO_SID    = os.environ["TWILIO_SID"]
TWILIO_TOKEN  = os.environ["TWILIO_TOKEN"]
FROM_WHATSAPP = "whatsapp:+14155238886"
TO_WHATSAPP   = "whatsapp:+994554400288"

VFS_URL = "https://www.vfsglobal.com/italy/azerbaijan/schedule-an-appointment.html"
CHECK_INTERVAL = 5

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/122.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}

def send_whatsapp(message: str):
    client = Client(TWILIO_SID, TWILIO_TOKEN)
    msg = client.messages.create(
        body=message,
        from_=FROM_WHATSAPP,
        to=TO_WHATSAPP
    )
    print(f"[{now()}] ✅ WhatsApp göndərildi: {msg.sid}")

def check_slot() -> bool:
    try:
        resp = requests.get(VFS_URL, headers=HEADERS, timeout=15)
        html = resp.text.lower()

        no_slot_keywords = [
            "no appointment",
            "no slots",
            "not available",
            "currently unavailable",
            "appointment not available",
            "no appointment slots available",
        ]
        for kw in no_slot_keywords:
            if kw in html:
                return False

        slot_keywords = [
            "book an appointment",
            "select date",
            "available",
            "choose a date",
            "calendar",
            "schedule",
        ]
        for kw in slot_keywords:
            if kw in html:
                return True

        return False

    except Exception as e:
        print(f"[{now()}] ⚠️  Xəta: {e}")
        return False

def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def main():
    print(f"[{now()}] 🚀 VFS İtaliya Slot İzləyici başladı!")
    print(f"[{now()}] 📱 Bildiriş gedəcək: {TO_WHATSAPP}")
    print(f"[{now()}] 🔄 Hər {CHECK_INTERVAL} saniyədən bir yoxlanır...\n")

    send_whatsapp(
        "✅ VFS İtaliya Slot İzləyici işə düşdü!\n"
        "Boş görüş yeri açılanda sizi dərhal xəbərdar edəcəyəm. 🇮🇹"
    )

    notified = False

    while True:
        print(f"[{now()}] 🔍 Yoxlanır...")
        slot_available = check_slot()

        if slot_available:
            if not notified:
                print(f"[{now()}] 🎉 SLOT TAPILDI! WhatsApp göndərilir...")
                send_whatsapp(
                    "🎉 *SLOT AÇILDI!*\n\n"
                    "🇮🇹 İtaliya VFS Bakı - görüş yeri mövcuddur!\n\n"
                    "⚡ Dərhal keçin:\n"
                    "https://www.vfsglobal.com/italy/azerbaijan/schedule-an-appointment.html\n\n"
                    "⏰ Tez olun, tez dolar!"
                )
                notified = True
        else:
            print(f"[{now()}] ❌ Slot yoxdur, növbəti yoxlama {CHECK_INTERVAL} saniyə sonra.")
            notified = False

        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
