from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from users.models import User


@shared_task
def deactivate_inactive_users():
    month = timezone.now() - timedelta(days=30)
    inactive_users = User.objects.filter(last_login__lte=month, is_active=True)

    if inactive_users.exists():
        inactive_users.update(is_active=False)
        print(f"Deactivated users")
    else:
        print("No inactive users found.")
