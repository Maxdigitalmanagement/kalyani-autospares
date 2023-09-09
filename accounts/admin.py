from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account,UserAddress

# Register your models here.

class AddressesInline(admin.TabularInline):  # Inline admin for variations
    model = UserAddress
    extra = 1


class UserAddressAdmin(UserAdmin):
    list_display = ('user', 'first_name', 'last_name', 'email')


class AccountAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'username', 'last_login','date_joined', 'is_active')
    list_display_links = ('email', 'first_name', 'last_name')
    readonly_fields = ('last_login', 'date_joined')
    ordering = ('-date_joined',)
    inlines = [AddressesInline]

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(Account,AccountAdmin)
admin.site.register(UserAddress)