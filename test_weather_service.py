#!/usr/bin/env python3
"""
Test script for the WeatherService
"""
import os
import sys
import django
from pathlib import Path
import json
from datetime import datetime

# Set up Django environment
sys.path.append(str(Path(__file__).parent))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "weather_awareness.settings")
django.setup()


from awareness.services import WeatherService

def test_weather_service():
    """Test the weather service directly"""
    print("Testing WeatherService...")
    
    # Create service instance
    weather_service = WeatherService()
    
    # Test locations
    locations = ["Dhaka", "Barisal", "Chittagong", "Rangpur"]
    
    # Get today's date
    today_str = datetime.now().strftime('%Y-%m-%d')
    
    print(f"Testing with today's date: {today_str}")
    
    # Test each location
    for location in locations:
        print(f"\nTesting location: {location}")
        
        try:
            # Test with string date
            weather_data = weather_service.get_weather_forecast(location, today_str)
            
            if weather_data:
                print(f"✓ Weather data retrieved successfully for {location}")
                print(f"  - Temperature: {weather_data['temperature']}°C")
                print(f"  - Condition: {weather_data['condition']}")
            else:
                print(f"✗ Failed to retrieve weather data for {location}")
                
        except Exception as e:
            print(f"✗ Error: {str(e)}")

if __name__ == "__main__":
    test_weather_service()
