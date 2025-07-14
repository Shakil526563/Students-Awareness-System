"""
WSGI config for weather_awareness project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'weather_awareness.settings')

application = get_wsgi_application()
