import os
import sys
import django

# Django muhitini sozlash
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
try:
    django.setup()
except Exception as e:
    print(f"Django sozlashda xatolik: {e}")
    sys.exit(1)

from django.conf import settings
import requests

def send_link(github_url):
    token = getattr(settings, 'TELEGRAM_BOT_TOKEN', None)
    admin_id = getattr(settings, 'ADMIN_CHAT_ID', None)

    if not token or token == 'YOUR_BOT_TOKEN_HERE':
        print("Xatolik: Telegram Bot Token config/settings.py faylida o'rnatilmagan!")
        return False

    text = (
        f"🚀 **LOYIHA GITHUBGA MUVAFFAQIYATLI YUKLANDI!**\n\n"
        f"🔗 **GitHub Havolasi:** {github_url}\n\n"
        f"⚡️ Elektrik sayt loyihasi to'liq versiyasi GitHub-ga yuklandi va tekshirishga tayyor."
    )
    
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    try:
        r = requests.post(url, data={"chat_id": admin_id, "text": text, "parse_mode": "Markdown"})
        if r.status_code == 200:
            print("\nMuvaffaqiyatli: Havola Telegram bot orqali yuborildi!")
            return True
        else:
            print(f"\nXatolik: Bot javob bermadi. Status code: {r.status_code}. Javob: {r.text}")
            return False
    except Exception as e:
        print(f"\nTelegram xatoligi: {e}")
        return False

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Foydalanish: python send_github_link.py <GITHUB_REPO_URL>")
        sys.exit(1)
    
    url = sys.argv[1]
    send_link(url)
