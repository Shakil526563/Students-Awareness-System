from django.urls import path
from .views import WeatherAwarenessView, HealthCheckView, WeatherAwarenessHistoryView

urlpatterns = [
    path('awareness/', WeatherAwarenessView.as_view(), name='weather_awareness'),
    path('health/', HealthCheckView.as_view(), name='health_check'),
    path('history/', WeatherAwarenessHistoryView.as_view(), name='awareness_history'),
]
