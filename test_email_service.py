#!/usr/bin/env python3
"""
Direct test of EmailService to debug email sending
"""
import os
import sys
import django
from pathlib import Path

# Set up Django environment
sys.path.append(str(Path(__file__).parent))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "weather_awareness.settings")
django.setup()

from awareness.services import EmailService

def test_email_service_directly():
    """Test the EmailService directly"""
    email_service = EmailService()
    
    # Mock weather data
    weather_data = {
        'temperature': 27,
        'feels_like': 31,
        'condition': 'Clouds',
        'description': 'overcast clouds',
        'humidity': 85,
        'wind_speed': 4.85
    }
    
    ai_message = "Test AI message for debugging email service."
    safety_recommendation = "Normal school attendance recommended"
    
    result = email_service.send_weather_awareness_email(
        guardian_email="shakil15-3816@diu.edu.bd",
        location="Rangpur",
        date="2025-07-05",
        weather_data=weather_data,
        ai_message=ai_message,
        safety_recommendation=safety_recommendation
    )
    
    print(f"\nDirect EmailService test result: {result}")
    return result

if __name__ == "__main__":
    test_email_service_directly()
