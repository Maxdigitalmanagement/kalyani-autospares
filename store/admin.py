from django.contrib import admin
from .models import Product, ProductGallery,Variation,ReviewRating
import admin_thumbnails

# Register your models here.

@admin_thumbnails.thumbnail('image')
class ProductGalleryInline(admin.TabularInline):
    model = ProductGallery
    extra = 1

class VariationInline(admin.TabularInline):  # Inline admin for variations
    model = Variation
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'selling_price', 'stock', 'category', 'modified_date', 'is_available')
    prepopulated_fields = {'slug':('product_name',)}
    inlines = [VariationInline, ProductGalleryInline]

class VariationAdmin(admin.ModelAdmin):
    list_display = ('Product', 'variation_category', 'variation_value', 'is_active')
    list_editable = ('is_active',)
    list_filter = ('Product', 'variation_category', 'variation_value')

admin.site.register(Product, ProductAdmin)
admin.site.register(Variation, VariationAdmin)
admin.site.register(ReviewRating)
admin.site.register(ProductGallery)