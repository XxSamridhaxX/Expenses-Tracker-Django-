from django.db import models
from django.contrib.auth.models import User

# Create your models here.

CATEGORY_CHOICES=[
    ('Food','Food'),
    ('Transport','Transport'),
    ('Bills','Bills'),
    ('Entertainment','Entertainment'),
    ('Other','Other')
]
# Choices is a list type which contains list of tuples
# tuple(value,label) where value is the thing that is gonna be stored and label is to show in human readable form

class Expense(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(max_length=100)
    amount=models.DecimalField(max_digits=10,decimal_places=2) 
    category=models.CharField(max_length=50,choices=CATEGORY_CHOICES)
    date=models.DateField()

    def __str__(self):
        return f"{self.title}-{self.amount}"