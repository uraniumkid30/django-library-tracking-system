from datetime import datetime, timedelta

from django.utils import timezone
from django.conf import settings


def get_due_date():
    return timezone.now().date() + timedelta(days=settings.DEFAULT_DUE_DAYS)