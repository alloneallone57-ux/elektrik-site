import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from main.models import Master, ServicePrice

def seed():
    # Seed Masters
    if not Master.objects.exists():
        Master.objects.create(name="Jasur Qodirov", experience=8, rating=4.9, specialization="Rozetka, Lyustra, Shchit", bio="Tajribali usta")
        Master.objects.create(name="Farhod Aliyev", experience=5, rating=5.0, specialization="EV Zaryadka, Smart Home", bio="Innovatsion yechimlar")
        Master.objects.create(name="Alisher Usmonov", experience=12, rating=4.8, specialization="Yuqori kuchlanish, Stalba", bio="Xavfsiz montaj")

    # Seed Prices
    if not ServicePrice.objects.exists():
        ServicePrice.objects.create(service_name="Rozetka o'rnatish", price=50000, unit="dona")
        ServicePrice.objects.create(service_name="Lyustra ulash", price=150000, unit="dona")
        ServicePrice.objects.create(service_name="EV Zaryadka montaji", price=300000, unit="dona")
        ServicePrice.objects.create(service_name="Kabel tortish (SIP)", price=5000, unit="metr")
        ServicePrice.objects.create(service_name="Avtomat almashtirish", price=40000, unit="dona")

    print("Seeding complete!")

if __name__ == "__main__":
    seed()
