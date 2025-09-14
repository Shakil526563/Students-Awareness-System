# Students Awareness System 🌤️



https://github.com/user-attachments/assets/f2ebeafd-7cef-409e-8e7a-89b15ba13a6b



A Django-based REST API system that provides weather awareness notifications for students and their guardians. The system uses AI-powered recommendations to generate safety messages based on weather conditions and automatically sends email notifications to guardians.

## Features ✨

- **Weather Forecast Integration**: Fetches real-time weather data using OpenWeatherMap API
- **AI-Powered Safety Recommendations**: Uses Groq AI to generate personalized safety messages
- **Email Notifications**: Automatically sends weather awareness emails to guardians
- **REST API**: Clean API endpoints for integration with frontend applications
- **Student Safety Focus**: Tailored recommendations for student safety during various weather conditions

## Tech Stack 🛠️

- **Backend**: Django 4.2.0 + Django REST Framework
- **Database**: SQLite (development)
- **AI Service**: Groq AI API
- **Weather Service**: OpenWeatherMap API
- **Email**: Django's built-in email system
- **Dependencies**: See `requirements.txt`

## Project Structure 📁

```
Students-Awareness-System/
├── awareness/                 # Main Django app
│   ├── models.py             # Database models
│   ├── views.py              # API views
│   ├── services.py           # Weather & AI services
│   ├── serializers.py        # DRF serializers
│   └── urls.py               # App URLs
├── weather_awareness/         # Django project settings
│   ├── settings.py           # Project configuration
│   ├── urls.py               # Main URL routing
│   └── wsgi.py               # WSGI configuration
├── requirements.txt          # Python dependencies
├── manage.py                 # Django management script
├── start.py                  # Server startup script
├── db.sqlite3                # SQLite database
└── API_DOCUMENTATION.md      # Detailed API docs
```

## Quick Start 🚀

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Shakil526563/Studends-Awarnes-System.git
   cd Studends-Awarnes-System
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment Configuration**
   
   Create a `.env` file in the root directory with the following variables:
   ```env
   SECRET_KEY=your-django-secret-key
   DEBUG=True
   WEATHER_API_KEY=your-openweathermap-api-key
   WEATHER_API_BASE_URL=https://api.openweathermap.org/data/2.5
   GROQ_API_KEY=your-groq-api-key
   EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_USE_TLS=True
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=your-app-password
   ```

4. **Database Setup**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Run the Server**
   ```bash
   # Option 1: Using the start script
   python start.py
   
   # Option 2: Using Django management command
   python manage.py runserver 127.0.0.1:8000
   ```

6. **Access the API**
   - Base URL: `http://127.0.0.1:8000/api/`
   - Health Check: `http://127.0.0.1:8000/api/health/`

## API Usage 📡

### Health Check
```bash
GET http://127.0.0.1:8000/api/health/
```

### Weather Awareness Request
```bash
POST http://127.0.0.1:8000/api/awareness/
Content-Type: application/json

{
    "location": "Barisal",
    "date": "2025-07-15",
    "email": "guardian@example.com"
}
```

**Response:**
```json
{
    "status": "success",
    "message": "Weather awareness email sent successfully",
    "data": {
        "id": 1,
        "location": "Barisal",
        "date": "2025-07-15",
        "weather_condition": "Clear sky",
        "temperature": 28.5,
        "ai_message": "Perfect weather for outdoor activities...",
        "safety_recommendation": "Apply sunscreen and stay hydrated",
        "email_sent": true
    }
}
```

## Configuration ⚙️

### Required API Keys

1. **OpenWeatherMap API**
   - Sign up at [OpenWeatherMap](https://openweathermap.org/api)
   - Get your free API key
   - Add to `.env` file as `WEATHER_API_KEY`

2. **Groq AI API**
   - Sign up at [Groq](https://groq.com/)
   - Get your API key
   - Add to `.env` file as `GROQ_API_KEY`

3. **Email Configuration**
   - Configure SMTP settings in `.env`
   - For Gmail, use App Passwords instead of regular passwords

## Testing 🧪

The project includes test files for various services:

```bash
# Test weather service
python test_weather_service.py

# Test Groq AI service
python test_groq_service.py

# Test email service
python test_email_service.py

# Test main feature
python test-feature.py
```

## Development 💻

### Adding New Features

1. **Models**: Add new models in `awareness/models.py`
2. **Views**: Create API views in `awareness/views.py`
3. **Services**: Add business logic in `awareness/services.py`
4. **URLs**: Register new endpoints in `awareness/urls.py`

### Database Migrations

```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate
```

### Admin Interface

```bash
# Create superuser
python manage.py createsuperuser

# Access admin at http://127.0.0.1:8000/admin/
```

## Deployment 🌐

### Production Checklist

- [ ] Set `DEBUG=False` in production
- [ ] Configure proper SECRET_KEY
- [ ] Set up production database (PostgreSQL recommended)
- [ ] Configure static files serving
- [ ] Set up HTTPS
- [ ] Configure production email backend
- [ ] Add proper CORS settings

### Environment Variables

Ensure all required environment variables are set in production:
- `SECRET_KEY`
- `DEBUG`
- `WEATHER_API_KEY`
- `GROQ_API_KEY`
- Email configuration variables

## Contributing 🤝

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License 📄

This project is open source and available under the [MIT License](LICENSE).

## Support 📞

For support, please open an issue on GitHub or contact the development team.

## Changelog 📝

### v1.0.0
- Initial release
- Weather forecast integration
- AI-powered safety recommendations
- Email notification system
- REST API endpoints

---

**Built with ❤️ for student safety and awareness**

