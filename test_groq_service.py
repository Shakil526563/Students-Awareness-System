#!/usr/bin/env python3
"""
Test script for the GroqService
"""
import os
import sys
import django
from pathlib import Path
import json
from datetime import datetime

sys.path.append(str(Path(__file__).parent))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "weather_awareness.settings")
django.setup()

# Import the service
from awareness.services import GroqService, WeatherService

def test_groq_service():
    """Test the Groq service directly"""
    print("Testing GroqService...")
    
    # Create service instances
    weather_service = WeatherService()
    groq_service = GroqService()
    
    # Test location
    location = "Dhaka"
    
    # Get today's date
    today_str = datetime.now().strftime('%Y-%m-%d')
    
    print(f"Testing with location: {location}, date: {today_str}")
    
    try:
        # First get weather data
        weather_data = weather_service.get_weather_forecast(location, today_str)
        
        if not weather_data:
            print("✗ Failed to get weather data for Groq test")
            return
            
        print(f"Weather data retrieved: {weather_data['condition']}, {weather_data['temperature']}°C")
        
        # Now test Groq
        print("Generating AI message using Groq...")
        ai_message = groq_service.generate_awareness_message(location, today_str, weather_data)
        
        if ai_message:
            print(f"✓ Successfully generated AI message ({len(ai_message)} characters)")
            print("\nMessage preview:")
            print("-" * 40)
            print(ai_message[:200] + "..." if len(ai_message) > 200 else ai_message)
            print("-" * 40)
        else:
            print("✗ Failed to generate AI message")
            
    except Exception as e:
        print(f"✗ Error: {str(e)}")

if __name__ == "__main__":
    test_groq_service()
