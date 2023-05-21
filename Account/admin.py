from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from Account.models import Account, Profile


class AdminAccountConfig(UserAdmin):
    model = Account
    search_fields = ('email', 'username')
    list_filter = ('email', 'username', 'is_active', 'is_superuser')
    list_display = ('email', 'username', 'is_active', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('email', 'username', 'display_name', 'picture')}),
        ('permissions', {'fields': ('is_active', 'is_superuser')})
    )
    add_fieldsets = [
        (None, {'classes': ('wide',), 'fields': ('email', 'display_name', 'username', 'password1', 'password2')})
    ]


admin.site.register(Account, AdminAccountConfig)
admin.site.register(Profile)

