from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

User = get_user_model()

class CustomUserAdmin(UserAdmin):
    # Redefine fieldsets for the change form
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('name', 'nickname', 'phone_number')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login',)}), # last_login is read-only
    )
    # Redefine add_fieldsets for the add form
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password', 'password2', 'name', 'nickname', 'phone_number'),
        }),
    )
    # Display custom fields in the list view
    list_display = ('email', 'name', 'nickname', 'is_staff', 'is_active')
    search_fields = ('email', 'name', 'nickname')
    ordering = ('email',)
    
    # Add last_login to readonly_fields
    readonly_fields = ('last_login',)

try:
    admin.site.unregister(User)
except admin.sites.AlreadyRegistered:
    pass # Already unregistered or not registered

# Register your CustomUser model with the custom admin class
admin.site.register(User, CustomUserAdmin)