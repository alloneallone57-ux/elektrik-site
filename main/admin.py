from django.contrib import admin
from .models import ServiceRequest, Material, StaffStatus, Master, ServicePrice, Review, MasterPortfolio, SEOMeta

@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'region', 'district', 'urgency', 'status', 'created_at')
    list_filter = ('status', 'region', 'urgency', 'created_at')
    search_fields = ('name', 'phone', 'district', 'mahalla', 'street')
    list_editable = ('status', 'urgency')
    fieldsets = (
        ('Mijoz ma\'lumotlari', {
            'fields': ('name', 'surname', 'phone', 'additional_phone', 'user_identity')
        }),
        ('Manzil (To\'liq)', {
            'fields': ('region', 'district', 'mahalla', 'street', 'house_number', 'latitude', 'longitude')
        }),
        ('Buyurtma tafsilotlari', {
            'fields': ('service_type', 'urgency', 'message', 'preferred_time', 'image')
        }),
        ('Holat va Ishchi biriktirish', {
            'fields': ('status', 'is_processed', 'assigned_to')
        }),
    )

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('service_name',)
    fieldsets = (
        ('O\'zbekcha (Default)', {'fields': ('service_name', 'material_list')}),
        ('Русский', {'fields': ('service_name_ru', 'material_list_ru')}),
        ('English', {'fields': ('service_name_en', 'material_list_en')}),
        ('Media', {'fields': ('image',)}),
    )

@admin.register(StaffStatus)
class StaffStatusAdmin(admin.ModelAdmin):
    list_display = ('total_staff', 'available_staff', 'updated_at')

@admin.register(Master)
class MasterAdmin(admin.ModelAdmin):
    list_display = ('name', 'experience', 'rating', 'is_active')
    list_editable = ('is_active',)
    fieldsets = (
        ('Asosiy', {'fields': ('name', 'image', 'experience', 'rating', 'is_active')}),
        ('Ixtisoslik (Translations)', {'fields': ('specialization', 'specialization_ru', 'specialization_en')}),
        ('Ma\'lumot (Translations)', {'fields': ('bio', 'bio_ru', 'bio_en')}),
    )

@admin.register(MasterPortfolio)
class MasterPortfolioAdmin(admin.ModelAdmin):
    list_display = ('master', 'title', 'created_at')
    list_filter = ('master',)
    fieldsets = (
        ('Asosiy', {'fields': ('master', 'image')}),
        ('Sarlavha', {'fields': ('title', 'title_ru', 'title_en')}),
        ('Tavsif', {'fields': ('description', 'description_ru', 'description_en')}),
    )

@admin.register(ServicePrice)
class ServicePriceAdmin(admin.ModelAdmin):
    list_display = ('service_name', 'price', 'unit')
    list_editable = ('price',)
    fieldsets = (
        ('Narx', {'fields': ('service_name', 'price')}),
        ('Xizmat nomi (Translations)', {'fields': ('service_name_ru', 'service_name_en')}),
        ('Birlik (Translations)', {'fields': ('unit', 'unit_ru', 'unit_en')}),
    )

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('master', 'rating', 'created_at')
    readonly_fields = ('created_at',)

@admin.register(SEOMeta)
class SEOMetaAdmin(admin.ModelAdmin):
    list_display = ('page_url', 'title')
    search_fields = ('page_url', 'title')
    fieldsets = (
        ('Sahifa', {'fields': ('page_url',)}),
        ('Sarlavha (Meta Title)', {'fields': ('title', 'title_ru', 'title_en')}),
        ('Tavsif (Meta Description)', {'fields': ('description', 'description_ru', 'description_en')}),
        ('Kalit so\'zlar (Keywords)', {'fields': ('keywords', 'keywords_ru', 'keywords_en')}),
    )
