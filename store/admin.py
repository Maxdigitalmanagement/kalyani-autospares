from django.contrib import admin
from .models import Product,Variation

# Register your models here.

class VariationInline(admin.TabularInline):  # Inline admin for variations
    model = Variation
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'selling_price', 'stock', 'category', 'modified_date', 'is_available')
    prepopulated_fields = {'slug':('product_name',)}
    inlines = [VariationInline]

class VariationAdmin(admin.ModelAdmin):
    list_display = ('Product', 'variation_category', 'variation_value', 'is_active')
    list_editable = ('is_active',)
    list_filter = ('Product', 'variation_category', 'variation_value')

admin.site.register(Product, ProductAdmin)
admin.site.register(Variation, VariationAdmin)