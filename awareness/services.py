import requests
import json
from datetime import datetime, timedelta
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from groq import Groq
import logging

logger = logging.getLogger(__name__)


class WeatherService:
    """Service class for weather API operations"""
    
    def __init__(self):
        self.api_key = settings.WEATHER_API_KEY
        self.base_url = settings.WEATHER_API_BASE_URL
    
    def get_weather_forecast(self, location, target_date):
        """
        Get weather forecast for a specific location and date.
        Returns weather data or None if not found.
        """
        try:
            # Get current weather first to validate location
            current_url = f"{self.base_url}/weather"
            current_params = {
                'q': location,
                'appid': self.api_key,
                'units': 'metric'
            }
            
            current_response = requests.get(current_url, params=current_params, timeout=10)
            
            if current_response.status_code != 200:
                logger.error(f"Weather API error: {current_response.status_code}")
                return None
            
            current_data = current_response.json()
            
            # Ensure target_date is a date object
            if isinstance(target_date, str):
                target_date = datetime.strptime(target_date, '%Y-%m-%d').date()
                
            # Calculate days difference
            today = datetime.now().date()
            days_diff = (target_date - today).days
            
            # If it's today or tomorrow, try to get more accurate forecast
            if days_diff <= 5:  # OpenWeatherMap 5-day forecast
                forecast_url = f"{self.base_url}/forecast"
                forecast_params = {
                    'q': location,
                    'appid': self.api_key,
                    'units': 'metric'
                }
                
                forecast_response = requests.get(forecast_url, params=forecast_params, timeout=10)
                
                if forecast_response.status_code == 200:
                    forecast_data = forecast_response.json()
                    
                    # Find the closest forecast to target date
                    target_datetime = datetime.combine(target_date, datetime.min.time())
                    
                    for forecast in forecast_data['list']:
                        forecast_datetime = datetime.fromtimestamp(forecast['dt'])
                        
                        # If we find a forecast for the target date
                        if forecast_datetime.date() == target_date:
                            return {
                                'location': current_data['name'],
                                'country': current_data['sys']['country'],
                                'date': target_date.strftime('%Y-%m-%d'),
                                'temperature': round(forecast['main']['temp']),
                                'feels_like': round(forecast['main']['feels_like']),
                                'condition': forecast['weather'][0]['main'],
                                'description': forecast['weather'][0]['description'],
                                'humidity': forecast['main']['humidity'],
                                'wind_speed': forecast['wind']['speed'],
                                'rain_probability': forecast.get('pop', 0) * 100 if 'pop' in forecast else 0
                            }
            
            # Fallback to current weather data with a note
            return {
                'location': current_data['name'],
                'country': current_data['sys']['country'],
                'date': target_date.strftime('%Y-%m-%d'),
                'temperature': round(current_data['main']['temp']),
                'feels_like': round(current_data['main']['feels_like']),
                'condition': current_data['weather'][0]['main'],
                'description': current_data['weather'][0]['description'],
                'humidity': current_data['main']['humidity'],
                'wind_speed': current_data['wind']['speed'],
                'rain_probability': 0,
                'note': 'Based on current weather conditions'
            }
            
        except requests.RequestException as e:
            logger.error(f"Weather API request failed: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Weather service error: {str(e)}")
            return None


class GroqService:
    """Service class for Groq AI operations"""
    
    def __init__(self):
        try:
            self.api_key = settings.GROQ_API_KEY
            self.client = Groq(api_key=self.api_key)
            self.use_fallback = False
        except Exception as e:
            logger.error(f"Failed to initialize Groq client: {str(e)}")
            self.use_fallback = True
    
    def generate_awareness_message(self, location, date, weather_data):
        """
        Generate AI-powered awareness message using Groq API.
        """
        try:
            if self.use_fallback:
                return self._generate_fallback_message(location, date, weather_data)
                
            # Prepare the prompt
            prompt = f"""
            Generate a concise, friendly awareness message for school students and their guardians in {location} for {date}.
            
            Weather Information:
            - Location: {weather_data['location']}
            - Temperature: {weather_data['temperature']}°C
            - Condition: {weather_data['condition']}
            - Description: {weather_data['description']}
            - Humidity: {weather_data['humidity']}%
            - Wind Speed: {weather_data['wind_speed']} m/s
            
            Please provide:
            1. A brief weather summary
            2. Safety recommendations for students
            3. Suggestions for what to carry/wear
            4. Whether attending school is safe or if precautions are needed
            
            Keep the message under 200 words, friendly, and actionable.
            """
            
            try:
                response = self.client.chat.completions.create(
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a helpful assistant that provides weather-based safety advice for school students. Your responses should be clear, practical, and caring."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    model="llama3-8b-8192",
                    temperature=0.7,
                    max_tokens=300
                )
            except Exception as e:
                logger.error(f"Groq API error: {str(e)}")
                return self._generate_fallback_message(location, date, weather_data)
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"Groq API error: {str(e)}")
            return self._generate_fallback_message(location, date, weather_data)
            
    def _generate_fallback_message(self, location, date, weather_data):
        """Generate a fallback message when Groq API is not available"""
        condition = weather_data['condition'].lower()
        temp = weather_data['temperature']
        
        # Basic templates based on weather condition
        if 'rain' in condition or 'shower' in condition or 'drizzle' in condition:
            return f"""Weather Alert for {location} on {date}: Rainy conditions expected with temperatures around {temp}°C.

Safety Recommendations:
- Carry an umbrella or raincoat
- Wear water-resistant shoes
- Be cautious on slippery roads and pavements
- Allow extra time for travel to school

School attendance is safe with proper rain gear. Students should bring a change of clothes if possible. Stay dry and warm!"""
            
        elif 'thunder' in condition or 'storm' in condition:
            return f"""Weather Alert for {location} on {date}: Thunderstorms expected with temperatures around {temp}°C.

Safety Recommendations:
- Consider delaying travel during heavy storms
- Stay indoors during lightning
- Avoid open areas and tall objects
- Keep electronic devices charged

If storms are severe, parents should use discretion regarding school attendance. Safety comes first!"""
            
        elif 'clear' in condition or 'sun' in condition:
            if temp > 35:
                return f"""Weather Alert for {location} on {date}: Hot and sunny conditions with temperatures around {temp}°C.

Safety Recommendations:
- Wear lightweight, loose-fitting clothing
- Apply sunscreen before going out
- Carry a water bottle to stay hydrated
- Seek shade during outdoor activities

School attendance is safe, but students should stay hydrated and avoid prolonged sun exposure."""
            else:
                return f"""Weather Alert for {location} on {date}: Pleasant sunny conditions with temperatures around {temp}°C.

Safety Recommendations:
- Wear comfortable clothing suitable for the temperature
- Consider sunscreen for outdoor activities
- Stay hydrated throughout the day

School attendance is safe with normal precautions. Enjoy the pleasant weather!"""
                
        else:
            # Default message for other weather conditions
            return f"""Weather Alert for {location} on {date}: {weather_data['description'].capitalize()} with temperatures around {temp}°C.

Safety Recommendations:
- Dress appropriately for the temperature
- Stay aware of changing weather conditions
- Follow standard safety practices

School attendance is generally safe. Please monitor local announcements for any updates."""


class EmailService:
    """Service class for email operations"""
    
    def send_weather_awareness_email(self, guardian_email, location, date, weather_data, ai_message, safety_recommendation):
        """
        Send weather awareness email to guardian.
        """
        try:
            subject = f"Weather Alert for {location} - {date}"
            print(f"[EmailService] Preparing to send email to: {guardian_email}")
            print(f"[EmailService] Using from: {settings.DEFAULT_FROM_EMAIL}")
            print(f"[EmailService] Email backend: {getattr(settings, 'EMAIL_BACKEND', None)}")
            print(f"[EmailService] Host: {getattr(settings, 'EMAIL_HOST', None)} Port: {getattr(settings, 'EMAIL_PORT', None)} TLS: {getattr(settings, 'EMAIL_USE_TLS', None)}")
            print(f"[EmailService] Subject: {subject}")
            # Create email content
            email_body = f"""
            Dear Guardian,

            This is a weather awareness notification for your child's school day.

            \U0001F4CD Location: {location}
            \U0001F4C5 Date: {date}
            \U0001F321\uFE0F Temperature: {weather_data['temperature']}°C (Feels like {weather_data.get('feels_like', weather_data['temperature'])}°C)
            \U0001F324\uFE0F Weather Condition: {weather_data['condition']} - {weather_data['description']}
            \U0001F4A7 Humidity: {weather_data['humidity']}%
            \U0001F4A8 Wind Speed: {weather_data['wind_speed']} m/s

            AI RECOMMENDATIONS:
            {ai_message}

            SAFETY LEVEL: {safety_recommendation}

            Please take necessary precautions to ensure your child's safety and comfort during their school day.

            Best regards,
            Student Weather Awareness System
            ---
            This is an automated message generated by our AI-powered weather awareness system.
            """
            print(f"[EmailService] Email body preview:\n{email_body[:200]}...\n---")
            email = EmailMessage(
                subject=subject,
                body=email_body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[guardian_email],
            )
            print("[EmailService] Sending email...")
            email.send()
            print(f"[EmailService] Email sent to {guardian_email}")
            logger.info(f"Weather awareness email sent to {guardian_email}")
            return True
        except Exception as e:
            print(f"[EmailService] Email sending failed: {e}")
            logger.error(f"Email sending failed: {str(e)}")
            return False


def determine_safety_recommendation(weather_data):
    """
    Determine safety recommendation based on weather conditions.
    """
    condition = weather_data['condition'].lower()
    temp = weather_data['temperature']
    wind_speed = weather_data['wind_speed']
    
    # High risk conditions
    if ('storm' in condition or 'thunder' in condition or 
        wind_speed > 15 or temp > 40 or temp < 0):
        return "High caution advised - consider online classes"
    
    # Moderate risk conditions
    elif ('rain' in condition or 'snow' in condition or 
          temp > 35 or temp < 5 or wind_speed > 10):
        return "Moderate caution advised - take proper precautions"
    
    # Low risk conditions
    else:
        return "Normal school attendance recommended"
