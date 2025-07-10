from django.contrib import admin
from .models import Medicine

# Register your models here.

@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = [
        'medicine_name',
        'manufacturer',
        'formula',
        'dose',
        'get_price_display',
        'get_rating_display',
        'emc_leaflet_url',
    ]
    list_filter = ['manufacturer', 'rating']
    search_fields = ['medicine_name', 'formula', 'manufacturer']
    list_per_page = 25
    ordering = ['medicine_name']
    
    # Custom column headers
    def get_price_display(self, obj):
        return obj.get_price_display()
    get_price_display.short_description = 'Price'
    
    def get_rating_display(self, obj):
        return obj.get_rating_display()
    get_rating_display.short_description = 'Rating (Demo only)'
    
    def dose(self, obj):
        return obj.dose
    dose.short_description = 'Dose & Quantity'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('medicine_name', 'formula', 'dose')
        }),
        ('Commercial Details', {
            'fields': ('manufacturer', 'price', 'rating', 'emc_leaflet_url')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )