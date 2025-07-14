from django.contrib import admin
from .models import WeatherAwareness


@admin.register(WeatherAwareness)
class WeatherAwarenessAdmin(admin.ModelAdmin):
    """Admin interface for WeatherAwareness model"""
    
    list_display = [
        'location', 
        'date', 
        'guardian_email', 
        'weather_condition', 
        'temperature',
        'safety_recommendation',
        'email_sent',
        'created_at'
    ]
    
    list_filter = [
        'weather_condition',
        'email_sent',
        'date',
        'created_at'
    ]
    
    search_fields = [
        'location',
        'guardian_email',
        'weather_condition'
    ]
    
    readonly_fields = [
        'created_at',
        'updated_at'
    ]
    
    ordering = ['-created_at']
    
    fieldsets = (
        ('Request Information', {
            'fields': ('location', 'date', 'guardian_email')
        }),
        ('Weather Data', {
            'fields': ('weather_condition', 'temperature')
        }),
        ('AI Response', {
            'fields': ('ai_message', 'safety_recommendation')
        }),
        ('Status', {
            'fields': ('email_sent',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
