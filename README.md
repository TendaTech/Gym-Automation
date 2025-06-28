# Gym Automation & Subscription Reminder System

A comprehensive gym management system with a React frontend and Django REST API backend, featuring member management, workout tracking, coach scheduling, and automated email notifications.

## 🚀 Features

### Frontend (React + TypeScript)
- **Modern UI**: Beautiful, responsive design with Tailwind CSS
- **Multi-Authentication**: Firebase Auth with email, phone, Google, Facebook, Twitter, Apple
- **Member Portal**: Dedicated dashboard for members to track workouts and sessions
- **Admin Dashboard**: Complete member management with statistics and analytics
- **Real-time Notifications**: Toast notifications for all user actions
- **Bulk Operations**: Excel/CSV import for member data
- **Responsive Design**: Mobile-first design that works on all devices

### Backend (Django REST API)
- **Complete REST API**: Full CRUD operations for all gym entities
- **Workout Management**: Plans, sessions, and progress tracking
- **Coach Scheduling**: Availability management and session booking
- **Email Automation**: Automated subscription reminders and notifications
- **Task Scheduling**: Celery-based background tasks
- **Admin Interface**: Django admin for easy management
- **API Documentation**: Swagger/OpenAPI documentation

## 🛠️ Tech Stack

### Frontend
- **React 18** + TypeScript
- **Tailwind CSS** for styling
- **Firebase Auth** for authentication
- **React Router DOM** for routing
- **React Hot Toast** for notifications
- **Lucide React** for icons
- **date-fns** for date handling
- **Vite** for build tooling

### Backend
- **Django 4.2** + Django REST Framework
- **PostgreSQL** (SQLite for development)
- **Celery + Redis** for task queue
- **SendGrid** for email services
- **JWT Authentication**
- **Pandas** for Excel/CSV processing
- **drf-spectacular** for API documentation

## 📋 Prerequisites

- **Node.js** (version 16.0 or higher)
- **Python** (version 3.8 or higher)
- **PostgreSQL** (for production) or SQLite (for development)
- **Redis** (for Celery task queue)
- **Git** for version control
- **Firebase account** (free tier available)
- **SendGrid account** for email services

## 🔧 Installation & Setup

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd gym-automation-system
```

### 2. Frontend Setup

```bash
# Install dependencies
npm install

# Create environment file
cp .env.example .env

# Configure Firebase credentials in .env
VITE_FIREBASE_API_KEY=your_firebase_api_key
VITE_FIREBASE_AUTH_DOMAIN=your_project.firebaseapp.com
VITE_FIREBASE_PROJECT_ID=your_project_id
VITE_FIREBASE_STORAGE_BUCKET=your_project.appspot.com
VITE_FIREBASE_MESSAGING_SENDER_ID=your_sender_id
VITE_FIREBASE_APP_ID=your_app_id

# Start development server
npm run dev
```

The frontend will be available at `http://localhost:5173`

### 3. Backend Setup

```bash
# Navigate to backend directory
cd backend-django

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create environment file
cp .env.example .env

# Configure environment variables in .env
SECRET_KEY=your_super_secret_key_here
DEBUG=True
DATABASE_URL=postgresql://user:pass@localhost:5432/gym_db
SENDGRID_API_KEY=your_sendgrid_api_key
REDIS_URL=redis://localhost:6379/0

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Load sample data (optional)
python manage.py loaddata fixtures/sample_members.json

# Start development server
python manage.py runserver
```

The API will be available at `http://localhost:8000`

### 4. Start Background Services

```bash
# In separate terminals:

# Start Celery worker
celery -A gym_automation worker --loglevel=info

# Start Celery beat (for scheduled tasks)
celery -A gym_automation beat --loglevel=info
```

## 📁 Project Structure

```
gym-automation-system/
├── src/                          # Frontend React app
│   ├── components/              # React components
│   │   ├── auth/               # Authentication components
│   │   ├── dashboard/          # Dashboard components
│   │   ├── layout/             # Layout components
│   │   └── members/            # Member management components
│   ├── contexts/               # React contexts
│   ├── hooks/                  # Custom React hooks
│   ├── lib/                    # External service configurations
│   ├── services/               # API services and business logic
│   ├── types/                  # TypeScript type definitions
│   └── data/                   # Sample data and constants
├── backend-django/              # Django REST API
│   ├── gym_automation/         # Main Django project
│   ├── apps/                   # Django apps
│   │   ├── members/           # Member management
│   │   ├── authentication/    # Custom authentication
│   │   └── core/              # Core utilities
│   ├── templates/             # Email templates
│   └── fixtures/              # Sample data
├── package.json                # Frontend dependencies
└── README.md                   # This file
```

## 🔌 API Integration

### Authentication
```javascript
// Login
const response = await fetch('http://localhost:8000/api/auth/login/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ email, password })
});

// Use JWT token in subsequent requests
const headers = {
  'Authorization': `Bearer ${accessToken}`,
  'Content-Type': 'application/json'
};
```

### Member Management
```javascript
// Get all members
const members = await fetch('http://localhost:8000/api/members/api/members/', {
  headers: headers
});

// Create member
const newMember = await fetch('http://localhost:8000/api/members/api/members/', {
  method: 'POST',
  headers: headers,
  body: JSON.stringify(memberData)
});
```

### Member Portal
```javascript
// Get member dashboard
const dashboard = await fetch('http://localhost:8000/api/members/api/portal/dashboard/', {
  headers: headers
});

// Check in to gym
await fetch('http://localhost:8000/api/members/api/checkins/checkin/', {
  method: 'POST',
  headers: headers
});
```

## 🏋️ Key Features

### Member Portal
- **Personal Dashboard**: View workout stats, upcoming sessions, and progress
- **Workout Tracking**: Log completed workouts with exercises, sets, and reps
- **Session Booking**: Book training sessions with available coaches
- **Check-in System**: Digital gym check-in/check-out with duration tracking
- **Progress Monitoring**: Track workout streaks, milestones, and achievements

### Admin Features
- **Member Management**: Complete CRUD operations for gym members
- **Bulk Operations**: Import members via Excel/CSV files
- **Coach Management**: Manage coach profiles, schedules, and availability
- **Workout Plans**: Create and assign workout plans to members
- **Email Automation**: Send subscription reminders, birthday wishes, and motivational emails
- **Analytics Dashboard**: View member statistics and gym performance metrics

### Email System
- **Subscription Reminders**: Automated emails 5 days before subscription expires
- **Birthday Wishes**: Personalized birthday greetings
- **Motivational Emails**: Weekly motivation for active members
- **Inactivity Alerts**: Re-engagement emails for inactive members
- **Workout Reminders**: Notifications for scheduled workouts

## 📊 Data Models

### Member
- Personal information (name, email, phone, birthday)
- Membership details (type, due date, status)
- Health information (height, weight, fitness goals)
- Progress tracking (milestones, notes)

### Coach
- Profile information and specializations
- Experience and certifications
- Availability schedule
- Hourly rates

### Workout Plan
- Plan details (name, description, difficulty)
- Sessions and exercises
- Duration and frequency

### Training Session
- Session details (title, type, date/time)
- Coach and participant management
- Status tracking

## 🔐 Authentication & Security

### Firebase Authentication
- Email/password authentication
- Social login (Google, Facebook, Twitter, Apple)
- Phone number authentication with SMS
- JWT token management

### API Security
- JWT-based authentication
- Role-based access control
- CORS configuration
- Input validation and sanitization

## 📧 Email Configuration

### SendGrid Setup
1. Create SendGrid account
2. Generate API key with full access
3. Verify sender identity
4. Configure environment variables

### Email Templates
Professional HTML email templates with:
- Responsive design
- Personalized content
- Call-to-action buttons
- Branding consistency

## 🧪 Testing

### Frontend Testing
```bash
# Run linting
npm run lint

# Build for production
npm run build
```

### Backend Testing
```bash
# Run all tests
python manage.py test

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```

### API Testing
- Swagger UI: `http://localhost:8000/api/docs/`
- ReDoc: `http://localhost:8000/api/redoc/`

## 🚀 Deployment

### Frontend Deployment (Vercel)
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel

# Set environment variables in Vercel dashboard
```

### Backend Deployment (Heroku)
```bash
# Create Heroku app
heroku create your-gym-api

# Set environment variables
heroku config:set SECRET_KEY=your_secret_key
heroku config:set DATABASE_URL=your_database_url

# Deploy
git push heroku main
heroku run python manage.py migrate
```

## 📱 Mobile Responsiveness

The application is fully responsive with:
- Mobile-first design approach
- Touch-friendly interface
- Collapsible navigation
- Optimized layouts for all screen sizes

## 🔧 Configuration

### Environment Variables

#### Frontend (.env)
```env
VITE_FIREBASE_API_KEY=your_firebase_api_key
VITE_FIREBASE_AUTH_DOMAIN=your_project.firebaseapp.com
VITE_FIREBASE_PROJECT_ID=your_project_id
VITE_API_BASE_URL=http://localhost:8000/api/members/api
```

#### Backend (.env)
```env
SECRET_KEY=your_django_secret_key
DEBUG=True
DATABASE_URL=postgresql://user:pass@localhost:5432/gym_db
SENDGRID_API_KEY=your_sendgrid_api_key
REDIS_URL=redis://localhost:6379/0
```

## 🐛 Troubleshooting

### Common Issues

1. **Firebase Authentication Errors**:
   - Verify environment variables are set correctly
   - Check Firebase console for proper provider configuration

2. **API Connection Issues**:
   - Ensure Django server is running on port 8000
   - Check CORS configuration in Django settings

3. **Email Not Sending**:
   - Verify SendGrid API key
   - Check sender verification status

4. **Database Errors**:
   - Ensure PostgreSQL is running
   - Run migrations: `python manage.py migrate`

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/new-feature`
3. Write tests for new functionality
4. Ensure all tests pass
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

---

**Ready to revolutionize your gym management! 💪🏋️‍♀️**