from django.contrib import admin
from .models import Category,Bike,PartBelongs

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('category_name',)}
    list_display = ('category_name', 'slug')

class BikeAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('bike_name',)}
    list_display = ('bike_name', 'slug')

class BelongsAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('belongsto',)}
    list_display = ('belongsto', 'slug')

admin.site.register(Category, CategoryAdmin)
admin.site.register(Bike,BikeAdmin)
admin.site.register(PartBelongs,BelongsAdmin)