from django.db import models
from django.contrib.auth.models import User

DIFFICULTY_CHOICES = [
    ('easy', 'Easy'),
    ('moderate', 'Moderate'),
    ('hard', 'Hard'),
]

class Route(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    distance = models.PositiveIntegerField(help_text="Distance in kilometers")
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']
