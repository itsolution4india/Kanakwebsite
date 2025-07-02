from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['name', 'number', 'location', 'is_verified', 'created_at']
    list_filter = ['is_verified', 'subscribe_sms', 'subscribe_email', 'subscribe_voice']
    search_fields = ['name', 'number', 'location']