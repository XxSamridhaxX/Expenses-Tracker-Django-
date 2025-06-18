from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from expenses.models import Expense
from datetime import date, timedelta
import random

class Command(BaseCommand):
    help = 'Generate dummy expense data for testing'

    def handle(self, *args, **kwargs):
        CATEGORY_CHOICES = [
            ('Food', 'Food'),
            ('Transport', 'Transport'),
            ('Bills', 'Bills'),
            ('Entertainment', 'Entertainment'),
            ('Other', 'Other'),
        ]

        titles = [
            'Grocery Shopping', 'Bus Ticket', 'Electric Bill', 'Movie Night',
            'Lunch', 'Taxi', 'Gas Bill', 'Netflix Subscription',
            'Gift Purchase', 'Random Expense'
        ]

        users = User.objects.all()
        if not users.exists():
            self.stdout.write(self.style.ERROR("⚠️  No users found. Please create at least one user."))
            return

        total_created = 0
        for user in users:
            for _ in range(20):  # 20 expenses per user
                Expense.objects.create(
                    user=user,
                    title=random.choice(titles),
                    amount=round(random.uniform(10.0, 500.0), 2),
                    category=random.choice([c[0] for c in CATEGORY_CHOICES]),
                    date=date.today() - timedelta(days=random.randint(0, 90))
                )
                total_created += 1

        self.stdout.write(self.style.SUCCESS(f"✅ Created {total_created} dummy expenses for {users.count()} users."))
