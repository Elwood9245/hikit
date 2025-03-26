from django.test import TestCase
from django.contrib.auth.models import User
from hikit.models import Route, Event, EventComment, Participation, UserProfile
from datetime import datetime, timedelta
from django.utils.timezone import make_aware

class ModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.profile = self.user.profile  # Auto-created via signal
        self.route = Route.objects.create(
            name="Test Route",
            description="Test route description",
            distance=10.5,
            elevation_gain=500,
            difficulty="Medium",
            created_by=self.user
        )
        self.event = Event.objects.create(
            route=self.route,
            organizer=self.user,
            title="Test Event",
            description="Test event description",
            date=make_aware(datetime.now() + timedelta(days=5)),
            max_participants=10
        )

    def test_route_str(self):
        self.assertEqual(str(self.route), "Test Route")

    def test_event_str(self):
        self.assertEqual(str(self.event), f"{self.event.title} - {self.route.name}")

    def test_event_can_join(self):
        self.assertTrue(self.event.can_join)

    def test_event_is_full(self):
        self.event.current_participants = 10
        self.assertTrue(self.event.is_full)

    def test_event_is_past(self):
        self.event.date = make_aware(datetime.now() - timedelta(days=1))
        self.event.save()
        self.assertTrue(self.event.is_past)

    def test_event_participation_percent(self):
        self.event.current_participants = 5
        self.assertEqual(self.event.participation_percent, 50.0)

    def test_user_profile_created(self):
        self.assertEqual(self.profile.user.username, 'testuser')

    def test_event_comment_str(self):
        comment = EventComment.objects.create(
            event=self.event,
            user=self.user,
            content="Test comment"
        )
        self.assertEqual(str(comment), f"Comment by {self.user.username} on {self.event.title}")

    def test_participation_unique(self):
        Participation.objects.create(event=self.event, user=self.user)
        with self.assertRaises(Exception):
            Participation.objects.create(event=self.event, user=self.user)  # Duplicate
