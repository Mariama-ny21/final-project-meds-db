
from django.contrib import admin
from django.utils.html import format_html
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
        'rating_stars',
        'emc_leaflet_url',
    ]

    def rating_stars(self, obj):
        try:
            # Use Django's floatformat:0 logic: round half away from zero
            rating = float(obj.rating)
            if rating >= 0:
                stars = int(rating + 0.5)
            else:
                stars = int(rating - 0.5)
        except (TypeError, ValueError):
            stars = 0
        if stars < 1:
            return 'No rating'
        if stars > 5:
            stars = 5
        star_html = ''.join([
            '<span style="color: #ffc107;">&#9733;</span>' for _ in range(stars)
        ])
        return format_html(star_html)
    rating_stars.short_description = 'Rating (Demo only)'
    rating_stars.allow_tags = True
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
    )