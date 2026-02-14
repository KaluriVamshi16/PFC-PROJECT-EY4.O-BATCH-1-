from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Expense(models.Model):

    CATEGORY_CHOICES = [
        ('Food', 'Food'),
        ('Travel', 'Travel'),
        ('Shopping', 'Shopping'),
        ('Bills', 'Bills'),
        ('Entertainment', 'Entertainment'),
        ('Health', 'Health'),
        ('Education', 'Education'),
        ('Other', 'Other'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="expenses")
    title = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    date = models.DateField(default=timezone.now)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.title} - ₹{self.amount}"


class Budget(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="budgets")
    category = models.CharField(max_length=100)
    monthly_limit = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ('user', 'category')  # Prevent duplicate budgets

    def __str__(self):
        return f"{self.user.username} - {self.category} Budget"


class Goal(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="goals")
    title = models.CharField(max_length=200)
    target_amount = models.DecimalField(max_digits=10, decimal_places=2)
    saved_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    deadline = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['deadline']

    def progress_percentage(self):
        if self.target_amount == 0:
            return 0
        return round((self.saved_amount / self.target_amount) * 100, 2)

    def remaining_amount(self):
        return self.target_amount - self.saved_amount

    def is_completed(self):
        return self.saved_amount >= self.target_amount

    def __str__(self):
        return self.title
