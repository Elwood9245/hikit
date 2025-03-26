from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.core.files.storage import default_storage

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
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_routes')
    saved_by = models.ManyToManyField(User, related_name='saved_routes', blank=True)
    completed_by = models.ManyToManyField(User, related_name='past_routes', blank=True)
    featured_image = models.ImageField(upload_to='route_images/', null=True, blank=True)  # 这里的upload_to值得是需要上传到这个文件夹中

    def __str__(self):
        return self.name

    def display_name(self):
        # <--!Dynamically generates formatted name without database storage-->
        return f"{self.name.title()} {self.distance}km | {self.elevation_gain}m"


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

    @property
    def can_join(self):
        return (
                self.status == 'planning' and
                self.current_participants < self.max_participants and
                self.date > timezone.now()
        )

    @property
    def is_full(self):
        return self.current_participants >= self.max_participants

    @property
    def is_past(self):
        return self.date < timezone.now()

    @property
    def participation_percent(self):
        return (self.current_participants / self.max_participants) * 100

    def __str__(self):
        return f"{self.title} - {self.route.name}"

class EventComment(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.event.title}"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)


class Participation(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='participants')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='participations')
    joined_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    class Meta:
        unique_together = ('event', 'user')


class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    profile_picture = models.ImageField(
        upload_to='profile_pics',
        null=True,
        blank=True,
        verbose_name="Profile Photo",
        help_text="Upload a square image (recommended 400x400px)"
    )

    def __str__(self):
        return f"{self.user.username}'s Profile"

    def save(self, *args, **kwargs):
        # Delete old file when updating
        if self.pk:
            old_file = UserProfile.objects.get(pk=self.pk).profile_picture
            if old_file and old_file != self.profile_picture:
                default_storage.delete(old_file.path)
        super().save(*args, **kwargs)

    @property
    def picture_url(self):
        if self.profile_picture:
            return self.profile_picture.url
        return '/static/image/default_profile.png'  # Default avatar
