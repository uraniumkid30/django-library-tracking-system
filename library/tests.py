from unittest.mock import patch


from django.test import TestCase, override_settings
from django.utils import timezone
from rest_framework.test import APIClient
from .tasks import check_overdue_loans
from .models import Loan, Book, User, Author, Member

# Create your tests here.


class MyLibraryTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.author = Author.objects.create(
            first_name="bobby",
            last_name="doe",
        )
        self.user = User.objects.create(username="bob")
        self.book = Book.objects.create(
            title="bookie",
            author=self.author,
            isbn="my isbn",
        )
        self.member = Member.objects.create(user=self.user)
        self.overdue_loan = Loan.objects.create(
            book=self.book,
            member=self.member,
            due_date=timezone.now() - timezone.timedelta(days=1),
            is_returned=False,
        )
        self.returned_loan = Loan.objects.create(
            book=self.book,
            member=self.member,
            due_date=timezone.now() - timezone.timedelta(days=1),
            is_returned=True,
        )
        self.active_loan = Loan.objects.create(
            book=self.book,
            member=self.member,
            due_date=timezone.now() + timezone.timedelta(days=1),
            is_returned=False,
        )

    @patch("libraary.tasks.send_email")
    @override_settings(CELERY_TASK_ALWAYS_EAGER=True)
    def test_overdue_loabs(self, mock_email):
        check_overdue_loans.delay()
        self.assertTrue(mock_email.called)
