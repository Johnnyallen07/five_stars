from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from django.contrib.auth.models import Group

admin.site.unregister(Group)


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    # Define which fields are displayed on the user detail page
    fieldsets = (
        (None, {'fields': ('username', 'password', 'image')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'subscriptions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )
    filter_horizontal = UserAdmin.filter_horizontal + ('subscriptions',)
    list_display = ('id', 'username', 'email', 'is_staff')  #


admin.site.register(CustomUser, CustomUserAdmin)
