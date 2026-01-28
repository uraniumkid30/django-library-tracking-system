from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone

from .models import Loan


@shared_task
def send_loan_notification(loan_id):
    try:
        loan = Loan.objects.get(id=loan_id)
        member_email = loan.member.user.email
        book_title = loan.book.title
        send_mail(
            subject="Book Loaned Successfully",
            message=f'Hello {loan.member.user.username},\n\nYou have successfully loaned "{book_title}".\nPlease return it by the due date.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[member_email],
            fail_silently=False,
        )
    except Loan.DoesNotExist:
        pass


@shared_task
def check_overdue_loans():
    over_due_loans = Loan.objects.filter(
        due_date__lt=timezone.now(),
        is_returned=False,
    ).select_related("book", "member__user")
    for loan in over_due_loans:
        user = loan.member.user
        book_title = loan.book.title
        send_mail(
            subject="Overdue Book Loan Notification",
            message=f'Hello {user.username},\n\nLoan on  "{book_title}" has Expired.\nPlease return it soon.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )
