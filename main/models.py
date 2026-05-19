from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import get_language

class ServiceRequest(models.Model):
    STATUS_CHOICES = [
        ('NEW', 'Yangi'),
        ('ACCEPTED', 'Qabul qilindi'),
        ('COMPLETED', 'Bajarildi'),
        ('REJECTED', 'Rad etildi'),
    ]
    name = models.CharField(max_length=100, verbose_name="Ismi")
    surname = models.CharField(max_length=100, verbose_name="Familiyasi", blank=True, null=True)
    phone = models.CharField(max_length=20, verbose_name="Telefon raqami")
    additional_phone = models.CharField(max_length=20, verbose_name="Qo'shimcha telefon raqami", blank=True, null=True)
    region = models.CharField(max_length=100, verbose_name="Viloyat", blank=True, null=True)
    district = models.CharField(max_length=100, verbose_name="Tuman/Shahar", blank=True, null=True)
    mahalla = models.CharField(max_length=100, verbose_name="Mahalla", blank=True, null=True)
    street = models.CharField(max_length=100, verbose_name="Ko'cha", blank=True, null=True)
    house_number = models.CharField(max_length=50, verbose_name="Uy/Xonadon raqami", blank=True, null=True)
    user_identity = models.CharField(max_length=100, verbose_name="Shaxs turi", blank=True, null=True)
    service_type = models.CharField(max_length=100, verbose_name="Xizmat turi", blank=True, null=True)
    urgency = models.CharField(
        max_length=20,
        choices=[('LOW', 'Oddiy'), ('MEDIUM', 'Muhim'), ('HIGH', 'Shoshilinch')],
        default='LOW',
        verbose_name="Shoshilinchlik darajasi"
    )
    message = models.TextField(verbose_name="Qo'shimcha izoh", blank=True, null=True)
    preferred_time = models.CharField(max_length=100, verbose_name="Qachon qulay?", blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, verbose_name="Kenglik (Latitude)")
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, verbose_name="Uzunlik (Longitude)")
    image = models.ImageField(upload_to='requests/', blank=True, null=True, verbose_name="Rasm (muammo tasviri)")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Murojaat vaqti")
    is_processed = models.BooleanField(default=False, verbose_name="Ko'rib chiqildi")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='NEW', verbose_name="Holati")
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='tasks', verbose_name="Ishchi")

    def __str__(self):
        return f"{self.name} - {self.phone}"

    class Meta:
        verbose_name = "Murojaat "
        verbose_name_plural = "Murojaatlar"
        ordering = ['-created_at']

class Material(models.Model):
    service_name = models.CharField(max_length=100, verbose_name="Xizmat nomi (UZ)")
    service_name_ru = models.CharField(max_length=100, verbose_name="Xizmat nomi (RU)", blank=True, null=True)
    service_name_en = models.CharField(max_length=100, verbose_name="Xizmat nomi (EN)", blank=True, null=True)
    
    material_list = models.TextField(verbose_name="Materiallar (UZ)")
    material_list_ru = models.TextField(verbose_name="Materiallar (RU)", blank=True, null=True)
    material_list_en = models.TextField(verbose_name="Materiallar (EN)", blank=True, null=True)
    
    image = models.ImageField(upload_to='materials/', blank=True, null=True, verbose_name="Rasm")

    @property
    def translated_service_name(self):
        lang = get_language()
        if lang == 'ru' and self.service_name_ru: return self.service_name_ru
        if lang == 'en' and self.service_name_en: return self.service_name_en
        return self.service_name

    @property
    def translated_material_list(self):
        lang = get_language()
        if lang == 'ru' and self.material_list_ru: return self.material_list_ru
        if lang == 'en' and self.material_list_en: return self.material_list_en
        return self.material_list

    def __str__(self):
        return self.service_name

class StaffStatus(models.Model):
    total_staff = models.IntegerField(default=0, verbose_name="Jami ishchilar soni")
    available_staff = models.IntegerField(default=0, verbose_name="Hozir bor ishchilar")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Xodimlar holati"
        verbose_name_plural = "Xodimlar holati"

class Master(models.Model):
    name = models.CharField(max_length=100, verbose_name="Ismi")
    image = models.ImageField(upload_to='masters/', blank=True, null=True, verbose_name="Rasmi")
    experience = models.IntegerField(default=0, verbose_name="Tajriba (yil)")
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=5.0, verbose_name="Reyting")
    
    specialization = models.CharField(max_length=200, verbose_name="Ixtisosligi (UZ)")
    specialization_ru = models.CharField(max_length=200, verbose_name="Ixtisosligi (RU)", blank=True, null=True)
    specialization_en = models.CharField(max_length=200, verbose_name="Ixtisosligi (EN)", blank=True, null=True)
    
    bio = models.TextField(blank=True, null=True, verbose_name="Ma'lumot (UZ)")
    bio_ru = models.TextField(blank=True, null=True, verbose_name="Ma'lumot (RU)")
    bio_en = models.TextField(blank=True, null=True, verbose_name="Ma'lumot (EN)")
    
    is_active = models.BooleanField(default=True, verbose_name="Faol")

    @property
    def translated_specialization(self):
        lang = get_language()
        if lang == 'ru' and self.specialization_ru: return self.specialization_ru
        if lang == 'en' and self.specialization_en: return self.specialization_en
        return self.specialization

    @property
    def translated_bio(self):
        lang = get_language()
        if lang == 'ru' and self.bio_ru: return self.bio_ru
        if lang == 'en' and self.bio_en: return self.bio_en
        return self.bio

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Usta"
        verbose_name_plural = "Ustalar"

class MasterPortfolio(models.Model):
    master = models.ForeignKey(Master, on_delete=models.CASCADE, related_name='portfolio', verbose_name="Usta")
    
    title = models.CharField(max_length=200, verbose_name="Ish nomi (UZ)")
    title_ru = models.CharField(max_length=200, verbose_name="Ish nomi (RU)", blank=True, null=True)
    title_en = models.CharField(max_length=200, verbose_name="Ish nomi (EN)", blank=True, null=True)
    
    image = models.ImageField(upload_to='portfolio/', verbose_name="Rasm")
    
    description = models.TextField(blank=True, null=True, verbose_name="Tavsif (UZ)")
    description_ru = models.TextField(blank=True, null=True, verbose_name="Tavsif (RU)")
    description_en = models.TextField(blank=True, null=True, verbose_name="Tavsif (EN)")
    
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def translated_title(self):
        lang = get_language()
        if lang == 'ru' and self.title_ru: return self.title_ru
        if lang == 'en' and self.title_en: return self.title_en
        return self.title

    @property
    def translated_description(self):
        lang = get_language()
        if lang == 'ru' and self.description_ru: return self.description_ru
        if lang == 'en' and self.description_en: return self.description_en
        return self.description

    def __str__(self):
        return f"{self.master.name} - {self.title}"

    class Meta:
        verbose_name = "Usta ishi"
        verbose_name_plural = "Ustalar ishlari"

class ServicePrice(models.Model):
    service_name = models.CharField(max_length=200, verbose_name="Xizmat nomi (UZ)")
    service_name_ru = models.CharField(max_length=200, verbose_name="Xizmat nomi (RU)", blank=True, null=True)
    service_name_en = models.CharField(max_length=200, verbose_name="Xizmat nomi (EN)", blank=True, null=True)
    
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Narxi")
    
    unit = models.CharField(max_length=50, default="dona", verbose_name="Birlik (UZ)")
    unit_ru = models.CharField(max_length=50, verbose_name="Birlik (RU)", blank=True, null=True)
    unit_en = models.CharField(max_length=50, verbose_name="Birlik (EN)", blank=True, null=True)

    @property
    def translated_service_name(self):
        lang = get_language()
        if lang == 'ru' and self.service_name_ru: return self.service_name_ru
        if lang == 'en' and self.service_name_en: return self.service_name_en
        return self.service_name

    @property
    def translated_unit(self):
        lang = get_language()
        if lang == 'ru' and self.unit_ru: return self.unit_ru
        if lang == 'en' and self.unit_en: return self.unit_en
        return self.unit

    def __str__(self):
        return f"{self.service_name} - {self.price} {self.unit}"

    class Meta:
        verbose_name = "Xizmat narxi"
        verbose_name_plural = "Xizmat narxlari"

class Review(models.Model):
    request = models.ForeignKey(ServiceRequest, on_delete=models.CASCADE, related_name='reviews', verbose_name="Ariza")
    master = models.ForeignKey(Master, on_delete=models.CASCADE, related_name='reviews', verbose_name="Usta")
    rating = models.IntegerField(default=5, verbose_name="Reyting (1-5)")
    comment = models.TextField(verbose_name="Izoh")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.master.name} - {self.rating}"

    class Meta:
        verbose_name = "Sharh"
        verbose_name_plural = "Sharhlar"

class SEOMeta(models.Model):
    page_url = models.CharField(max_length=255, unique=True, verbose_name="Sahifa URL")
    
    title = models.CharField(max_length=255, verbose_name="Meta Title (UZ)")
    title_ru = models.CharField(max_length=255, verbose_name="Meta Title (RU)", blank=True, null=True)
    title_en = models.CharField(max_length=255, verbose_name="Meta Title (EN)", blank=True, null=True)
    
    description = models.TextField(verbose_name="Meta Description (UZ)")
    description_ru = models.TextField(verbose_name="Meta Description (RU)", blank=True, null=True)
    description_en = models.TextField(verbose_name="Meta Description (EN)", blank=True, null=True)
    
    keywords = models.TextField(verbose_name="Keywords (UZ)")
    keywords_ru = models.TextField(verbose_name="Keywords (RU)", blank=True, null=True)
    keywords_en = models.TextField(verbose_name="Keywords (EN)", blank=True, null=True)

    @property
    def translated_title(self):
        lang = get_language()
        if lang == 'ru' and self.title_ru: return self.title_ru
        if lang == 'en' and self.title_en: return self.title_en
        return self.title

    @property
    def translated_description(self):
        lang = get_language()
        if lang == 'ru' and self.description_ru: return self.description_ru
        if lang == 'en' and self.description_en: return self.description_en
        return self.description

    @property
    def translated_keywords(self):
        lang = get_language()
        if lang == 'ru' and self.keywords_ru: return self.keywords_ru
        if lang == 'en' and self.keywords_en: return self.keywords_en
        return self.keywords

    def __str__(self):
        return self.page_url

    class Meta:
        verbose_name = "SEO Meta Teg"
        verbose_name_plural = "SEO Meta Teglar"

class TelegramUser(models.Model):
    chat_id = models.CharField(max_length=100, unique=True, verbose_name="Chat ID")
    phone = models.CharField(max_length=20, unique=True, verbose_name="Telefon raqami")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.phone} ({self.chat_id})"

    class Meta:
        verbose_name = "Telegram foydalanuvchi"
        verbose_name_plural = "Telegram foydalanuvchilar"
