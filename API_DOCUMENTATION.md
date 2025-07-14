# API Documentation

## Student Weather Awareness System API

### Base URL
```
http://127.0.0.1:8000/api/
```

### Authentication
No authentication required for this demo version.

---

## Endpoints

### 1. Health Check
**GET** `/health/`

Check if the API is running.

**Response:**
```json
{
    "status": "healthy",
    "message": "Student Weather Awareness System is running",
    "version": "1.0.0"
}
```

---

### 2. Weather Awareness Request
**POST** `/awareness/`

Generate weather awareness message and send email notification.

**Request Body:**
```json
{
    "location": "Barisal",
    "date": "2025-07-15",
    "email": "guardian@example.com"
}
```

**Request Parameters:**
- `location` (string, required): City or village name (2+ characters, letters only)
- `date` (string, required): Date in YYYY-MM-DD format (today or future)
- `email` (string, required): Valid guardian email address

**Success Response (200):**
```json
{
    "status": "success",
    "message": "Weather awareness notification sent successfully",
    "weather_data": {
        "location": "Barisal",
        "country": "BD",
        "date": "2025-07-15",
        "temperature": 28,
        "feels_like": 31,
        "condition": "Light Rain",
        "description": "light rain",
        "humidity": 85,
        "wind_speed": 3.2,
        "rain_probability": 70
    },
    "ai_message": "Light rain is expected in Barisal tomorrow. Please ensure your child carries an umbrella or raincoat to school. The temperature will be comfortable at 28°C, but the high humidity might make it feel warmer. Consider packing an extra set of clothes in case they get wet. School attendance is safe with proper rain gear.",
    "safety_recommendation": "Moderate caution advised - take proper precautions",
    "email_sent": true
}
```

**Error Response (400) - Validation Error:**
```json
{
    "status": "error",
    "message": "Invalid input data",
    "errors": {
        "location": ["Location name must be at least 2 characters long"],
        "date": ["Date cannot be in the past"],
        "email": ["Please enter a valid email address"]
    }
}
```

**Error Response (404) - Location Not Found:**
```json
{
    "status": "error",
    "message": "Unable to fetch weather data for the specified location. Please check the location name and try again."
}
```

---

### 3. Request History
**GET** `/history/`

Get paginated history of weather awareness requests.

**Query Parameters:**
- `page` (integer, optional): Page number (default: 1)
- `page_size` (integer, optional): Items per page (default: 10, max: 50)

**Response:**
```json
{
    "status": "success",
    "data": [
        {
            "id": 1,
            "location": "Barisal",
            "date": "2025-07-15",
            "guardian_email": "guardian@example.com",
            "weather_condition": "Light Rain",
            "temperature": 28.0,
            "safety_recommendation": "Moderate caution advised - take proper precautions",
            "email_sent": true,
            "created_at": "2025-07-02 10:30:00"
        }
    ],
    "pagination": {
        "page": 1,
        "page_size": 10,
        "total_count": 1,
        "total_pages": 1
    }
}
```

---

## Error Codes

- **200**: Success
- **400**: Bad Request (validation errors)
- **404**: Not Found (location not found)
- **500**: Internal Server Error

---

## Testing the API

### Using curl:
```bash
# Health check
curl http://127.0.0.1:8000/api/health/

# Weather awareness request
curl -X POST http://127.0.0.1:8000/api/awareness/ \
  -H "Content-Type: application/json" \
  -d '{"location": "Barisal", "date": "2025-07-15", "email": "guardian@example.com"}'

# History
curl http://127.0.0.1:8000/api/history/
```

### Using Python:
```python
import requests
import json
from datetime import datetime, timedelta

# Base URL
base_url = "http://127.0.0.1:8000/api"

# Health check
response = requests.get(f"{base_url}/health/")
print(response.json())

# Weather awareness request
tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
data = {
    "location": "Barisal",
    "date": tomorrow,
    "email": "guardian@example.com"
}

response = requests.post(
    f"{base_url}/awareness/",
    json=data,
    headers={'Content-Type': 'application/json'}
)
print(response.json())
```

---

## Setup Required

1. **Environment Variables** (in `.env` file):
   - `GROQ_API_KEY`: Get from https://console.groq.com/
   - `WEATHER_API_KEY`: Get from https://openweathermap.org/api
   - `EMAIL_HOST_USER`: Your Gmail address
   - `EMAIL_HOST_PASSWORD`: Your Gmail app password

2. **API Keys Setup**:
   - **Groq API**: Sign up at Groq Cloud, create API key
   - **OpenWeatherMap**: Sign up for free account, get API key
   - **Gmail**: Enable 2-factor auth, create app password

3. **Running the Server**:
   ```bash
   python manage.py runserver
   ```

The API will be available at `http://127.0.0.1:8000/api/`
