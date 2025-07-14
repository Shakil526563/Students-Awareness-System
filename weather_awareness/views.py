from django.http import JsonResponse
from django.shortcuts import render


def home_view(request):
    """Home page view - provides API information"""
    return JsonResponse({
        'title': 'Student Weather Awareness System',
        'version': '1.0.0',
        'status': 'running',
        'endpoints': {
            'health_check': '/api/health/',
            'weather_awareness': '/api/awareness/',
            'request_history': '/api/history/',
            'admin_panel': '/admin/'
        },
        'documentation': {
            'health_check': {
                'method': 'GET',
                'description': 'Check if the API is running'
            },
            'weather_awareness': {
                'method': 'POST',
                'description': 'Generate weather awareness message and send email notification',
                'required_fields': {
                    'location': 'City name (e.g., "Dhaka")',
                    'date': 'Date in YYYY-MM-DD format',
                    'email': 'Guardian email address'
                },
                'example': {
                    'location': 'Dhaka',
                    'date': '2025-07-15',
                    'email': 'guardian@example.com'
                }
            },
            'request_history': {
                'method': 'GET',
                'description': 'Get paginated history of weather awareness requests',
                'query_parameters': {
                    'page': 'Page number (default: 1)',
                    'page_size': 'Items per page (default: 10, max: 50)'
                }
            }
        },
        'features': [
            'Real-time weather data from OpenWeatherMap',
            'AI-powered safety recommendations using Groq',
            'Email notifications to guardians',
            'Request history tracking',
            'Location-based weather forecasts'
        ]
    }, json_dumps_params={'indent': 2})


def api_documentation_view(request):
    """API documentation view"""
    return render(request, 'api_docs.html')
