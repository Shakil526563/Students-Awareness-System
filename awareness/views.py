from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .serializers import WeatherAwarenessSerializer, WeatherAwarenessResponseSerializer
from .services import WeatherService, GroqService, EmailService, determine_safety_recommendation
from .models import WeatherAwareness
import logging

logger = logging.getLogger(__name__)


@method_decorator(csrf_exempt, name='dispatch')
class WeatherAwarenessView(APIView):
    """
    API endpoint to generate weather awareness messages and send email notifications.
    """
    
    def post(self, request):
        """
        Handle POST request for weather awareness.
        
        Expected payload:
        {
            "location": "Barisal",
            "date": "2025-07-15",
            "email": "guardian@example.com"
        }
        """
        try:
            # Validate input data
            serializer = WeatherAwarenessSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({
                    'status': 'error',
                    'message': 'Invalid input data',
                    'errors': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
            
            validated_data = serializer.validated_data
            location = validated_data['location']
            target_date = validated_data['date']
            guardian_email = validated_data['email']
            
            # Initialize services
            weather_service = WeatherService()
            groq_service = GroqService()
            email_service = EmailService()
            
            # Fetch weather data
            weather_data = weather_service.get_weather_forecast(location, target_date)
            if not weather_data:
                return Response({
                    'status': 'error',
                    'message': 'Unable to fetch weather data for the specified location. Please check the location name and try again.'
                }, status=status.HTTP_404_NOT_FOUND)
            
            # Generate AI awareness message
            ai_message = groq_service.generate_awareness_message(location, target_date, weather_data)
            
            # Determine safety recommendation
            safety_recommendation = determine_safety_recommendation(weather_data)
            
            # Send email notification
            email_sent = email_service.send_weather_awareness_email(
                guardian_email, location, target_date, weather_data, ai_message, safety_recommendation
            )
            
            # Save to database
            awareness_record = WeatherAwareness.objects.create(
                location=location,
                date=target_date,
                guardian_email=guardian_email,
                weather_condition=weather_data['condition'],
                temperature=weather_data['temperature'],
                ai_message=ai_message,
                safety_recommendation=safety_recommendation,
                email_sent=email_sent
            )
            
            # Prepare response
            response_data = {
                'status': 'success',
                'message': 'Weather awareness notification sent successfully' if email_sent else 'Weather data processed but email sending failed',
                'weather_data': weather_data,
                'ai_message': ai_message,
                'safety_recommendation': safety_recommendation,
                'email_sent': email_sent
            }
            
            return Response(response_data, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Weather awareness processing error: {str(e)}")
            return Response({
                'status': 'error',
                'message': 'An internal error occurred while processing your request. Please try again later.',
                'error_details': str(e) if logger.level == logging.DEBUG else None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def get(self, request):
        """
        Handle GET request to provide API information.
        """
        return Response({
            'message': 'Student Weather Awareness System API',
            'description': 'POST to this endpoint with location, date, and guardian email to receive weather awareness notifications',
            'required_fields': {
                'location': 'City or village name (string)',
                'date': 'Target date in YYYY-MM-DD format',
                'email': 'Guardian email address'
            },
            'example_request': {
                'location': 'Barisal',
                'date': '2025-07-15',
                'email': 'guardian@example.com'
            }
        })


class HealthCheckView(APIView):
    """
    Simple health check endpoint.
    """
    
    def get(self, request):
        """
        Health check endpoint to verify API is running.
        """
        return Response({
            'status': 'healthy',
            'message': 'Student Weather Awareness System is running',
            'version': '1.0.0'
        })


class WeatherAwarenessHistoryView(APIView):
    """
    View to get history of weather awareness requests.
    """
    
    def get(self, request):
        """
        Get paginated history of weather awareness requests.
        """
        try:
            # Get query parameters
            page = int(request.GET.get('page', 1))
            page_size = min(int(request.GET.get('page_size', 10)), 50)  # Max 50 items per page
            
            # Calculate offset
            offset = (page - 1) * page_size
            
            # Get total count
            total_count = WeatherAwareness.objects.count()
            
            # Get paginated results
            records = WeatherAwareness.objects.all()[offset:offset + page_size]
            
            # Serialize data
            records_data = []
            for record in records:
                records_data.append({
                    'id': record.id,
                    'location': record.location,
                    'date': record.date.strftime('%Y-%m-%d'),
                    'guardian_email': record.guardian_email,
                    'weather_condition': record.weather_condition,
                    'temperature': record.temperature,
                    'safety_recommendation': record.safety_recommendation,
                    'email_sent': record.email_sent,
                    'created_at': record.created_at.strftime('%Y-%m-%d %H:%M:%S')
                })
            
            return Response({
                'status': 'success',
                'data': records_data,
                'pagination': {
                    'page': page,
                    'page_size': page_size,
                    'total_count': total_count,
                    'total_pages': (total_count + page_size - 1) // page_size
                }
            })
            
        except Exception as e:
            logger.error(f"History retrieval error: {str(e)}")
            return Response({
                'status': 'error',
                'message': 'Failed to retrieve history'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
