from django.db import models
from django.contrib.auth.models import AbstractUser

class Student(AbstractUser):
    student_name = models.CharField(max_length=100, blank=True)
    student_id = models.IntegerField(unique=True, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True)
    birth_date = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True)

    class Meta:
        db_table = 'students'

