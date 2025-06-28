# Gym Automation System - Django REST API Backend

A comprehensive Django REST API backend for the Gym Automation & Subscription Reminder System, providing member management, workout tracking, coach scheduling, and automated email notifications.

## 🚀 Features

- **Complete RESTful API**: Full CRUD operations for all gym entities
- **Member Portal**: Dedicated member dashboard with workout tracking
- **Workout Management**: Plans, sessions, and progress tracking
- **Coach Scheduling**: Availability management and session booking
- **Email Automation**: Automated subscription reminders and notifications
- **Bulk Operations**: Excel/CSV import for members and data
- **Task Scheduling**: Celery-based background tasks
- **Authentication**: JWT-based authentication with role management
- **Admin Interface**: Django admin for easy management
- **API Documentation**: Swagger/OpenAPI documentation

## 🛠️ Tech Stack

- **Framework**: Django 4.2 + Django REST Framework
- **Database**: PostgreSQL (SQLite for development)
- **Task Queue**: Celery + Redis
- **Email Service**: SendGrid
- **Authentication**: Django REST Framework JWT
- **File Processing**: Pandas for Excel/CSV handling
- **API Documentation**: drf-spectacular (Swagger)
- **Environment**: python-decouple for configuration

## 📋 Prerequisites

- **Python** (version 3.8 or higher)
- **pip** (Python package installer)
- **PostgreSQL** (for production) or SQLite (for development)
- **Redis** (for Celery task queue)
- **Git** for version control
- A **SendGrid account** for email services

## 🔧 Installation & Setup

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd gym-automation-system/backend-django
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Configuration

Create a `.env` file in the backend-django directory:

```env
# Django Settings
SECRET_KEY=your_super_secret_key_here_make_it_long_and_random
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

# Database Configuration
DATABASE_URL=postgresql://username:password@localhost:5432/gym_automation_db
# For development with SQLite, comment out DATABASE_URL

# Email Configuration (SendGrid)
SENDGRID_API_KEY=your_sendgrid_api_key_here
FROM_EMAIL=noreply@yourgym.com
FROM_NAME=Your Gym Name

# Redis Configuration (for Celery)
REDIS_URL=redis://localhost:6379/0

# CORS Settings
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173,http://127.0.0.1:3000,http://127.0.0.1:5173

# Celery Settings
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# Frontend URL (for email templates)
FRONTEND_URL=http://localhost:5173
```

### 5. Database Setup

#### For Development (SQLite)
```bash
# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Load sample data (optional)
python manage.py loaddata fixtures/sample_members.json
```

#### For Production (PostgreSQL)
```bash
# Install PostgreSQL and create database
createdb gym_automation_db

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

### 6. Start the Development Server

```bash
# Start Django development server
python manage.py runserver

# In a separate terminal, start Celery worker
celery -A gym_automation worker --loglevel=info

# In another terminal, start Celery beat (for scheduled tasks)
celery -A gym_automation beat --loglevel=info
```

The API will be available at `http://localhost:8000`

## 📁 Project Structure

```
backend-django/
├── gym_automation/          # Main Django project
│   ├── settings/           # Settings modules
│   ├── urls.py            # Main URL configuration
│   ├── wsgi.py            # WSGI configuration
│   └── celery.py          # Celery configuration
├── apps/
│   ├── members/           # Member management app
│   │   ├── models.py      # All data models
│   │   ├── serializers.py # DRF serializers
│   │   ├── views.py       # API views and viewsets
│   │   ├── urls.py        # App URLs
│   │   ├── tasks.py       # Celery tasks
│   │   ├── filters.py     # Django filters
│   │   └── admin.py       # Admin interface
│   ├── authentication/    # Custom authentication
│   └── core/              # Core utilities
├── templates/             # Email templates
├── fixtures/              # Sample data
├── requirements.txt       # Python dependencies
├── manage.py             # Django management script
└── README.md             # This file
```

## 🔌 API Endpoints

### Authentication
```
POST /api/auth/login/          # Login with email/password
POST /api/auth/register/       # Register new user
POST /api/auth/refresh/        # Refresh JWT token
POST /api/auth/logout/         # Logout user
```

### Members Management
```
GET    /api/members/api/members/           # List all members
POST   /api/members/api/members/           # Create new member
GET    /api/members/api/members/{id}/      # Get member details
PUT    /api/members/api/members/{id}/      # Update member
DELETE /api/members/api/members/{id}/      # Delete member
GET    /api/members/api/members/stats/     # Get member statistics
POST   /api/members/api/members/bulk_upload/ # Bulk upload via Excel/CSV
GET    /api/members/api/members/{id}/dashboard/ # Member dashboard
```

### Coaches Management
```
GET    /api/members/api/coaches/           # List all coaches
POST   /api/members/api/coaches/           # Create new coach
GET    /api/members/api/coaches/{id}/      # Get coach details
GET    /api/members/api/coaches/{id}/schedule/ # Get coach schedule
GET    /api/members/api/coaches/{id}/availability/ # Check availability
```

### Workout Management
```
GET    /api/members/api/workout-plans/     # List workout plans
POST   /api/members/api/workout-plans/     # Create workout plan
GET    /api/members/api/workout-logs/      # List workout logs
POST   /api/members/api/workout-logs/      # Log workout
```

### Training Sessions
```
GET    /api/members/api/training-sessions/ # List training sessions
POST   /api/members/api/training-sessions/ # Create session
POST   /api/members/api/training-sessions/{id}/join/ # Join session
POST   /api/members/api/training-sessions/{id}/leave/ # Leave session
```

### Member Portal
```
GET    /api/members/api/portal/dashboard/  # Member dashboard
POST   /api/members/api/checkins/checkin/  # Check in to gym
POST   /api/members/api/checkins/checkout/ # Check out from gym
```

### Email Management
```
POST   /api/members/api/emails/send/       # Send emails
GET    /api/members/api/emails/logs/       # Get email logs
POST   /api/members/api/emails/send-reminders/ # Send subscription reminders
```

## 📊 Data Models

### Core Models

#### Member Model
```python
class Member(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    subscription_due_date = models.DateField()
    birthday = models.DateField(null=True, blank=True)
    membership_type = models.CharField(max_length=50, default='basic')
    is_active = models.BooleanField(default=True)
    # ... additional fields for health, fitness goals, etc.
```

#### Coach Model
```python
class Coach(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    specializations = models.JSONField(default=list)
    experience_years = models.PositiveIntegerField(default=0)
    hourly_rate = models.DecimalField(max_digits=8, decimal_places=2)
    is_available = models.BooleanField(default=True)
```

#### WorkoutPlan Model
```python
class WorkoutPlan(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=255)
    difficulty_level = models.CharField(max_length=20)
    duration_weeks = models.PositiveIntegerField()
    sessions_per_week = models.PositiveIntegerField()
    created_by = models.ForeignKey(Coach, on_delete=models.CASCADE)
```

## 📧 Email System

### Automated Email Types

1. **Subscription Reminders**: Sent 5 days before subscription expires
2. **Motivational Emails**: Weekly motivation for active members
3. **Birthday Wishes**: Sent on member's birthday
4. **Inactivity Alerts**: Sent to members inactive for 7+ days
5. **Workout Reminders**: Reminders for scheduled workouts
6. **Session Reminders**: Training session notifications

### Email Templates

Professional HTML email templates located in `templates/emails/`:
- `subscription_reminder.html/txt`
- `motivational_email.html/txt`
- `birthday_wish.html/txt`
- `inactivity_alert.html/txt`

## 🏋️ Member Portal Features

### Dashboard
- Current workout plan
- Recent workout history
- Upcoming training sessions
- Workout streak tracking
- Progress statistics

### Workout Tracking
- Log completed workouts
- Track exercises, sets, reps
- Rate workout difficulty
- Add personal notes

### Session Management
- View available training sessions
- Book sessions with coaches
- Cancel bookings
- View session history

### Check-in System
- Digital gym check-in/check-out
- Track gym visit duration
- Automatic attendance logging

## 📈 Bulk Operations

### Excel/CSV Import

Upload member data via Excel or CSV files:

```python
# Required columns for member import:
- full_name (required)
- email (required)
- subscription_due_date (required)
- phone (optional)
- birthday (optional)
- membership_type (optional, defaults to 'basic')
- is_active (optional, defaults to True)
```

Example CSV format:
```csv
full_name,email,subscription_due_date,phone,birthday,membership_type,is_active
John Doe,john@example.com,2024-12-31,+1234567890,1990-01-15,premium,true
Jane Smith,jane@example.com,2024-11-30,,1985-05-20,basic,true
```

## 🔐 Authentication & Permissions

### User Roles
- **Admin**: Full access to all features
- **Coach**: Manage workout plans, sessions, view assigned members
- **Member**: Access personal dashboard, book sessions, log workouts

### JWT Authentication
- Access tokens expire in 24 hours
- Refresh tokens for seamless experience
- Role-based access control

## 🧪 Testing

### API Testing with Swagger
Visit `http://localhost:8000/api/docs/` for interactive API documentation

### Sample Data
```bash
# Load sample data
python manage.py loaddata fixtures/sample_members.json

# Create test users
python manage.py shell
>>> from django.contrib.auth.models import User
>>> from apps.members.models import Member, Coach
>>> # Create test data
```

### Running Tests
```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test apps.members

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```

## 🚀 Deployment

### Environment Variables for Production

```env
DEBUG=False
SECRET_KEY=your_production_secret_key
DATABASE_URL=postgresql://user:pass@host:port/dbname
SENDGRID_API_KEY=your_sendgrid_key
REDIS_URL=redis://redis-host:6379/0
ALLOWED_HOSTS=yourdomain.com,api.yourdomain.com
```

### Deploy to Heroku

```bash
# Install Heroku CLI and login
heroku create your-gym-api

# Set environment variables
heroku config:set SECRET_KEY=your_secret_key
heroku config:set DATABASE_URL=your_database_url
heroku config:set SENDGRID_API_KEY=your_sendgrid_key

# Deploy
git push heroku main
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

### Deploy to DigitalOcean/AWS

1. Set up server with Python, PostgreSQL, Redis
2. Clone repository and install dependencies
3. Configure environment variables
4. Set up Gunicorn and Nginx
5. Configure Celery as system service

## 📱 Frontend Integration

### API Base URL
```javascript
const API_BASE_URL = 'http://localhost:8000/api/members/api';
```

### Authentication Headers
```javascript
const headers = {
  'Authorization': `Bearer ${accessToken}`,
  'Content-Type': 'application/json',
};
```

### Example API Calls
```javascript
// Get member dashboard
const response = await fetch(`${API_BASE_URL}/portal/dashboard/`, {
  headers: headers
});

// Log workout
const workoutData = {
  workout_session: sessionId,
  date: '2024-12-15',
  duration_minutes: 45,
  completed: true,
  rating: 4
};

await fetch(`${API_BASE_URL}/workout-logs/`, {
  method: 'POST',
  headers: headers,
  body: JSON.stringify(workoutData)
});
```

## 🔧 Configuration

### Celery Tasks Schedule
```python
# In gym_automation/celery.py
app.conf.beat_schedule = {
    'send-subscription-reminders': {
        'task': 'apps.members.tasks.send_subscription_reminders',
        'schedule': 86400.0,  # Daily
    },
    'send-motivational-emails': {
        'task': 'apps.members.tasks.send_motivational_emails',
        'schedule': 604800.0,  # Weekly
    },
    # ... more scheduled tasks
}
```

### Database Optimization
- Indexed fields for fast queries
- Select related for efficient joins
- Pagination for large datasets

## 🐛 Troubleshooting

### Common Issues

1. **Database Connection Errors**:
   ```bash
   # Check PostgreSQL status
   sudo systemctl status postgresql
   
   # Verify database exists
   psql -l
   ```

2. **Celery Not Working**:
   ```bash
   # Check Redis connection
   redis-cli ping
   
   # Verify Celery workers
   celery -A gym_automation inspect active
   ```

3. **Email Not Sending**:
   ```bash
   # Test SendGrid API key
   python manage.py shell
   >>> from django.core.mail import send_mail
   >>> send_mail('Test', 'Message', 'from@example.com', ['to@example.com'])
   ```

### Debug Mode
```python
# In settings/development.py
DEBUG = True
LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}
```

## 📚 API Documentation

### Swagger UI
- **URL**: `http://localhost:8000/api/docs/`
- **Features**: Interactive API testing, request/response examples
- **Authentication**: JWT token support

### ReDoc
- **URL**: `http://localhost:8000/api/redoc/`
- **Features**: Clean documentation layout

### Schema Export
```bash
# Generate OpenAPI schema
python manage.py spectacular --file schema.yml
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/new-feature`
3. Write tests for new functionality
4. Ensure all tests pass: `python manage.py test`
5. Commit changes: `git commit -am 'Add new feature'`
6. Push to branch: `git push origin feature/new-feature`
7. Submit pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Check the API documentation at `/api/docs/`
- Review the troubleshooting section
- Check Django and DRF documentation

---

**Ready to power your gym! 💪**