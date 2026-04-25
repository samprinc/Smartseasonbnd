from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Field, FieldUpdate

# 1. Custom User Admin (Shows roles in the table!)
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_superuser')
    # Add 'role' to the editable fields in the admin panel
    fieldsets = UserAdmin.fieldsets + (
        ('System Role', {'fields': ('role',)}),
    )

# 2. Advanced Field Admin
@admin.register(Field)
class FieldAdmin(admin.ModelAdmin):
    # What columns to show in the table
    list_display = ('name', 'crop_type', 'stage', 'get_status', 'assigned_to', 'planting_date')
    # Add a sidebar to filter by stage or assigned agent
    list_filter = ('stage', 'assigned_to', 'crop_type')
    # Add a search bar
    search_fields = ('name', 'crop_type')
    
    # Expose your @property method to the Django Admin table
    def get_status(self, obj):
        return obj.current_status
    get_status.short_description = 'Health Status'

# 3. Advanced Field Updates Admin
@admin.register(FieldUpdate)
class FieldUpdateAdmin(admin.ModelAdmin):
    list_display = ('field', 'stage_at_update', 'created_at', 'short_notes')
    list_filter = ('stage_at_update', 'created_at')
    search_fields = ('field__name', 'notes')
    
    # Truncate notes so they don't break the table UI if an agent writes an essay
    def short_notes(self, obj):
        return (obj.notes[:50] + '...') if len(obj.notes) > 50 else obj.notes
    short_notes.short_description = 'Update Notes'