from django.db import models
from users.models import User
# Create your models here.

class Post(models.Model):
    POST_TYPE_CHOICES = [
        ('lost', 'Lost Item'),
        ('found', 'Found Item'),
    ]
    # Reference to the student who created the post
    user = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 1})

    # Type of the post: Lost or Found
    post_type = models.CharField(max_length=10, choices=POST_TYPE_CHOICES)

    # Post Details
    item_name = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='post_photos/')
    event_date = models.DateField()
    event_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)
    is_visible = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.post_type.title()} post by {self.user.username} at {self.location}"

    class Meta:
        db_table = 'posts'  # custom table name (optional)
        ordering = ['-created_at']

