import requests
from django.conf import settings

def send_to_admin(name, surname, phone, region, user_identity, service, message="Yo'q", preferred_time="Noma'lum",
                  additional_phone="", district="", mahalla="", street="", house_number="", urgency="LOW"):
    """
    Adminga yangi ariza haqida to'liq xabar yuborish
    """
    token = getattr(settings, 'TELEGRAM_BOT_TOKEN', None)
    admin_id = getattr(settings, 'ADMIN_CHAT_ID', None)

    if not token or token == 'YOUR_BOT_TOKEN_HERE':
        print("Xatolik: Telegram Bot Token o'rnatilmagan!")
        return False

    urgency_emoji = {'LOW': '🟢 Oddiy', 'MEDIUM': '🟡 Muhim', 'HIGH': '🔴 FAVQULODDA 🚨'}.get(urgency, urgency)

    text = (
        f"⚡️ **YANGI BUYURTMA QABUL QILINDI!**\n\n"
        f"👤 **Mijoz:** {name} {surname or ''}\n"
        f"📞 **Tel:** {phone}\n"
    )
    if additional_phone:
        text += f"📞 **Qo'shimcha tel:** {additional_phone}\n"

    text += (
        f"🏢 **Shaxs turi:** {user_identity or 'Jismoniy'}\n"
        f"⚠️ **Muhimlik darajasi:** {urgency_emoji}\n\n"
        f"📍 **Manzil tafsilotlari:**\n"
        f"▫️ **Viloyat:** {region}\n"
        f"▫️ **Tuman/Shahar:** {district or 'Noma\'lum'}\n"
        f"▫️ **Mahalla:** {mahalla or 'Noma\'lum'}\n"
        f"▫️ **Ko'cha:** {street or 'Noma\'lum'}\n"
        f"▫️ **Uy:** {house_number or 'Noma\'lum'}\n\n"
        f"🛠 **Xizmat turi:** {service}\n"
        f"⏱ **Qulay vaqt:** {preferred_time}\n"
        f"📝 **Izoh:** {message}\n"
    )
    
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    try:
        requests.post(url, data={"chat_id": admin_id, "text": text, "parse_mode": "Markdown"})
        return True
    except Exception as e:
        print(f"Telegram xatoligi: {e}")
        return False

def send_status_update(chat_id, order_id, status):
    """
    Mijozga buyurtma holati o'zgargani haqida xabar yuborish
    """
    token = getattr(settings, 'TELEGRAM_BOT_TOKEN', None)
    if not token or token == 'YOUR_BOT_TOKEN_HERE':
        return False

    status_txt = {
        'ACCEPTED': "✅ Qabul qilindi. Usta tez orada siz bilan bog'lanadi.",
        'COMPLETED': "🎉 Bajarildi. Xizmatimizdan foydalanganingiz uchun rahmat!",
        'REJECTED': "❌ Rad etildi. Noqulaylik uchun uzr so'raymiz."
    }

    text = (
        f"🔔 **Buyurtma holati o'zgardi!**\n\n"
        f"🆔 Buyurtma raqami: #{order_id}\n"
        f"📊 Holati: {status_txt.get(status, status)}\n\n"
        f"🤖 @ElectroPro_Bot orqali kuzatishda davom eting."
    )

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    try:
        requests.post(url, data={"chat_id": chat_id, "text": text, "parse_mode": "Markdown"})
        return True
    except Exception as e:
        print(f"Telegram client notification error: {e}")
        return False
