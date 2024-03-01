# grades/models.py
from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100)
    score = models.PositiveIntegerField()
    email = models.EmailField(null=True, blank=True)
    email_sent = models.BooleanField(default=False)
