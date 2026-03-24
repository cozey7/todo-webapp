from django.core.mail import send_mail
from django.utils import timezone
from django.contrib.auth.models import User
from .models import Task
from django.conf import settings

def send_daily_reminders():
    """
    Background job to send reminders of tasks due today for each user.
    """
    today = timezone.now().date()
    users = User.objects.filter(is_active=True).prefetch_related('tasks')
    
    for user in users:
        tasks_due_today = user.tasks.filter(due_date=today, completed=False)
        
        if tasks_due_today.exists():
            message = f"Hello {user.username},\n\nYou have {tasks_due_today.count()} tasks due today:\n\n"
            for task in tasks_due_today:
                message += f"- {task.title}\n"
            
            send_mail(
                'Your Daily TODO Reminder',
                message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=True,
            )
            print(f"Sent reminder to {user.username}")
        else:
            print(f"No tasks due today for {user.username}")
