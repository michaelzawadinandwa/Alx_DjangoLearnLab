from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    """
    Admin configuration for the custom user model.
    Extends Django's UserAdmin to include the custom fields (date_of_birth, profile_photo).
    """
    
    # Fields displayed in the list view
    list_display = ('username', 'email', 'first_name', 'last_name', 'date_of_birth', 'is_staff', 'is_active')
    
    # Fields that can be filtered
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'date_joined')
    
    # Fields used for searching
    search_fields = ('username', 'email', 'first_name', 'last_name')
    
    # Fieldsets for the change form (edit view)
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal Info', {
            'fields': ('first_name', 'last_name', 'date_of_birth', 'profile_photo')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Important Dates', {
            'fields': ('last_login', 'date_joined')
        }),
    )
    
    # Fieldsets for the add form (create view)
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
        ('Personal Info', {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'date_of_birth', 'profile_photo'),
        }),
        ('Permissions', {
            'classes': ('wide',),
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
    )
    
    # Default ordering
    ordering = ('email',)
    
    # Filter horizontal for many-to-many fields
    filter_horizontal = ('groups', 'user_permissions')
