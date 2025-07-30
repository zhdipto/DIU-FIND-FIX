from django.db import models
from users.models import User

# Create your models here.

class Report(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 1})

    category = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=100)
    event_date = models.DateField()
    event_time = models.TimeField()
    photo = models.ImageField(upload_to='report_photos/', blank=True, null=True)


    # Boolean status: False = Unsolved, True = Solved
    status = models.BooleanField(default=False)

    is_visible = models.BooleanField(default=False)
    approved_by = models.CharField(max_length=100, blank=True, null=True)

    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        status_text = "Solved" if self.status else "Unsolved"
        return f"{status_text} Report by {self.user.username} at {self.location}"

    class Meta:
        db_table = 'reports'
        ordering = ['-submitted_at']
