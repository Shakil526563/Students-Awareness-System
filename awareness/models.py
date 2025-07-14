from django.db import models


class WeatherAwareness(models.Model):
    """Model to store weather awareness requests and responses"""
    location = models.CharField(max_length=100)
    date = models.DateField()
    guardian_email = models.EmailField()
    weather_condition = models.CharField(max_length=100, blank=True)
    temperature = models.FloatField(null=True, blank=True)
    ai_message = models.TextField(blank=True)
    safety_recommendation = models.CharField(max_length=200, blank=True)
    email_sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'weather_awareness'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.location} - {self.date} - {self.guardian_email}"
