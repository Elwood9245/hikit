from django.db import models
from django.contrib.auth.models import User

STATUS_CHOICES = [
    ('planning', 'Planning'),
    ('open', 'Open for Registration'),
    ('full', 'Full'),
    ('completed', 'Completed'),
    ('canceled', 'Canceled'),
]

class Route(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    distance = models.DecimalField(max_digits=6, decimal_places=2)  # 公里
    elevation_gain = models.PositiveIntegerField()  # 米
    difficulty = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    featured_image = models.ImageField(upload_to='route_images/', null=True, blank=True)

    def __str__(self):
        return self.name

class Event(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='events')
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organized_events')
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    max_participants = models.PositiveIntegerField(default=10)
    current_participants = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planning')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.route.name}"

class Participation(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='participants')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='participations')
    joined_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    class Meta:
        unique_together = ('event', 'user')

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True)
    hiking_experience = models.CharField(max_length=100, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    emergency_contact = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"