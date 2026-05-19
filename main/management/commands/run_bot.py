from django.core.management.base import BaseCommand
from django.conf import settings
from main.models import TelegramUser, ServiceRequest
import telebot # pyTelegramBotAPI kutubxonasi ishlatiladi
from telebot import types

class Command(BaseCommand):
    help = 'Telegram botni ishga tushirish'

    def handle(self, *args, **options):
        token = settings.TELEGRAM_BOT_TOKEN
        if not token or token == 'YOUR_BOT_TOKEN_HERE':
            self.stdout.write(self.style.ERROR('Bot token o\'rnatilmagan!'))
            return

        bot = telebot.TeleBot(token)

        @bot.message_handler(commands=['start'])
        def start(message):
            markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
            button = types.KeyboardButton("📱 Telefon raqamni yuborish", request_contact=True)
            markup.add(button)
            
            bot.send_message(
                message.chat.id, 
                "Assalomu alaykum! ElectroPro botiga xush kelibsiz.\n"
                "Buyurtmalaringizni kuzatish uchun telefon raqamingizni yuboring.",
                reply_markup=markup
            )

        @bot.message_handler(content_types=['contact'])
        def contact(message):
            if message.contact is not None:
                phone = message.contact.phone_number
                if not phone.startswith('+'):
                    phone = '+' + phone
                
                chat_id = str(message.chat.id)
                
                # Foydalanuvchini bazaga saqlash yoki yangilash
                tg_user, created = TelegramUser.objects.update_or_create(
                    phone=phone,
                    defaults={'chat_id': chat_id, 'is_active': True}
                )
                
                bot.send_message(
                    message.chat.id, 
                    f"Rahmat! Sizning {phone} raqamingiz ro'yxatga olindi.\n"
                    "Endi buyurtmangiz holati o'zgarganda sizga xabar yuboramiz.",
                    reply_markup=types.ReplyKeyboardRemove()
                )
                
                # Mavjud buyurtmalarni tekshirish
                orders = ServiceRequest.objects.filter(phone__icontains=phone.replace('+', ''))
                if orders.exists():
                    txt = "Sizning buyurtmalaringiz:\n\n"
                    for order in orders:
                        status_map = {
                            'NEW': '🆕 Yangi',
                            'ACCEPTED': '✅ Qabul qilingan',
                            'COMPLETED': '🎉 Bajarilgan',
                            'REJECTED': '❌ Rad etilgan'
                        }
                        txt += f"🆔 #{order.id} - {order.service_type}\n📊 Holati: {status_map.get(order.status, order.status)}\n\n"
                    bot.send_message(message.chat.id, txt)
                else:
                    bot.send_message(message.chat.id, "Hozircha sizda faol buyurtmalar yo'q.")

        self.stdout.write(self.style.SUCCESS('Bot ishga tushdi...'))
        bot.polling(none_stop=True)
