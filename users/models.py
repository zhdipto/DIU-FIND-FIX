from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        (1, 'Student'),
        (2, 'Admin'),
        (3, 'Super Admin'),
    )
    
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, default=1)

    name = models.CharField(max_length=100, blank=True)
    student_id = models.CharField(max_length=30, blank=True, null=True, unique=True)
    employee_id = models.CharField(max_length=30, blank=True, null=True, unique=True)
    phone_number = models.CharField(max_length=15, blank=True)
    birth_date = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    department = models.CharField(max_length=50, blank=True)
    last_updated_by = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='updated_users'
    )

    def save(self, *args, **kwargs):
        if self.role == 1 and self.student_id:
            self.username = self.student_id
        elif self.role in [2, 3] and self.employee_id:
            self.username = self.employee_id
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'user'

