# Multiuser TODO List Web App

A production-quality, modular TODO application built with Django and JavaScript.

## Features
- Task management (CRUD)
- Multiuser support with Token-based Authentication
- Filter tasks by "All" or "Due Today"
- Scheduled daily reminders via email (simulated in console)

## Setup Instructions

1.  **Clone the repository and enter the directory.**
2.  **Create a virtual environment and install dependencies:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install django djangorestframework django-environ django-cors-headers django-q2
    ```
3.  **Create a `.env` file from the following template:**
    ```env
    DEBUG=True
    SECRET_KEY=your-secret-key
    ALLOWED_HOSTS=localhost,127.0.0.1
    DEFAULT_FROM_EMAIL=todo@example.com
    ```
4.  **Run Migrations:**
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```
5.  **Create a Superuser (optional, for admin access):**
    ```bash
    python manage.py createsuperuser
    ```

## Running the Application

1.  **Start the Django Q Cluster (for background tasks):**
    ```bash
    python manage.py qcluster
    ```
2.  **Start the Web Server:**
    ```bash
    python manage.py runserver
    ```
3.  **Visit `http://localhost:8000` in your browser.**

## Daily Reminders

The reminder system is implemented using **Django Q2**. 

### How to Schedule Reminders
To schedule the daily reminder job to run every morning at 8 AM:
1.  Access the Django shell: `python manage.py shell`
2.  Run the following code:
    ```python
    from django_q.tasks import schedule
    from tasks.tasks import send_daily_reminders

    schedule('tasks.tasks.send_daily_reminders',
             schedule_type='D',
             repeats=-1)
    ```

### Testing Reminders Manually
You can trigger a reminder send immediately from the Django shell:
```python
from tasks.tasks import send_daily_reminders
send_daily_reminders()
```
The email content will be printed to the terminal console where the server or qcluster is running.

## Merged PR Log

- Initial log entry placeholder
- cozey7 2026-03-24 Update theming
- zachkfan 2026-03-24 Changed variable name
