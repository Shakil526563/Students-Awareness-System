from rest_framework import serializers
from django.core.validators import validate_email
from datetime import datetime, date
import re


class WeatherAwarenessSerializer(serializers.Serializer):
    """Serializer for weather awareness request"""
    location = serializers.CharField(
        max_length=100,
        required=True,
        help_text="City or village name"
    )
    date = serializers.DateField(
        required=True,
        help_text="Date in YYYY-MM-DD format"
    )
    email = serializers.EmailField(
        required=True,
        help_text="Guardian's email address"
    )

    def validate_location(self, value):
        """Validate location name"""
        if not value or len(value.strip()) < 2:
            raise serializers.ValidationError("Location name must be at least 2 characters long")
        
        # Allow letters, spaces, hyphens, and apostrophes
        if not re.match(r"^[a-zA-Z\s\-']+$", value.strip()):
            raise serializers.ValidationError("Location name can only contain letters, spaces, hyphens, and apostrophes")
        
        return value.strip().title()

    def validate_date(self, value):
        """Validate date - should be today or future date"""
        if value < date.today():
            raise serializers.ValidationError("Date cannot be in the past")
        return value

    def validate_email(self, value):
        """Validate email format"""
        try:
            validate_email(value)
        except:
            raise serializers.ValidationError("Please enter a valid email address")
        return value.lower()


class WeatherAwarenessResponseSerializer(serializers.Serializer):
    """Serializer for weather awareness response"""
    status = serializers.CharField()
    message = serializers.CharField()
    weather_data = serializers.DictField()
    ai_message = serializers.CharField()
    safety_recommendation = serializers.CharField()
