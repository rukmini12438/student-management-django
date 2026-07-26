# 🎓 VidyaTrack

A full-featured school/student management system built with Django. VidyaTrack lets admins manage student records, track fees, and monitor school activity through a live dashboard — with a complete authentication system including password reset.

## Features

- **Student Management (CRUD)** — add, view, edit, and delete student records with detailed profiles (academic info, contact details, parent/guardian info, photo upload)
- **Fee Management** — track fee records per student, mark payments as paid, view pending vs. collected totals
- **Authentication** — user registration, login, logout, and forgot-password flow with email-based reset links
- **Live Dashboard** — real-time stats (total students, departments, revenue) and interactive charts (Chart.js) showing monthly revenue and student admissions, driven by live database queries
- **Admin Panel** — full Django admin integration for managing students, departments, and fees

## Tech Stack

- **Backend:** Django 6.0, Python 3.14
- **Database:** SQLite (development)
- **Frontend:** HTML, Bootstrap 5, Chart.js, Font Awesome
- **Auth:** Django's built-in authentication system

## Setup Instructions

1. Clone the repository
```bash
   git clone https://github.com/rukmini12438/student-management-django.git
   cd student-management-django
```

2. Create and activate a virtual environment
```bash
   python -m venv .venv
   .venv\Scripts\activate
```

3. Install dependencies
```bash
   pip install -r requirements.txt
```

4. Run migrations
```bash
   python manage.py migrate
```

5. Create a superuser
```bash
   python manage.py createsuperuser
```

6. Run the development server
```bash
   python manage.py runserver
```

7. Open http://127.0.0.1:8000/ in your browser

## Roadmap / Future Improvements

- REST API layer (Django REST Framework)
- Attendance tracking
- Exam/results management
- Deployment to production (Render/Railway)

## Author

**Rukmini** — B.Tech CSE student, aspiring Full-Stack Django Developer
[GitHub](https://github.com/rukmini12438)
