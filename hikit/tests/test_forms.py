from django.test import TestCase
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from hikit.forms import RouteForm, EventForm, UserProfileForm, EventCommentForm
from hikit.models import Route, Event, EventComment, UserProfile
from datetime import datetime, timedelta

class RouteFormTests(TestCase):
    def test_valid_route_form(self):
        form_data = {
            'name': 'Test Trail',
            'description': 'A great hike',
            'distance': 10.5,
            'elevation_gain': 400,
            'difficulty': 'Easy'
        }
        form = RouteForm(data=form_data)
        self.assertTrue(form.is_valid())

class EventFormTests(TestCase):
    def test_valid_event_form(self):
        future_date = datetime.now() + timedelta(days=1)
        form_data = {
            'title': 'Mountain Meetup',
            'description': 'Let\'s hike together!',
            'date': future_date.strftime('%Y-%m-%dT%H:%M'),
            'max_participants': 10,
            'status': 'open',
        }
        form = EventForm(data=form_data)
        self.assertTrue(form.is_valid())

class UserProfileFormTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')


    def test_large_profile_picture_rejected(self):
        # Create a dummy file over 2MB
        big_file = SimpleUploadedFile("big.jpg", b"a" * (2 * 1024 * 1024 + 1), content_type="image/jpeg")
        form = UserProfileForm(files={'profile_picture': big_file}, user=self.user)
        self.assertFalse(form.is_valid())
        self.assertIn('profile_picture', form.errors)

class EventCommentFormTests(TestCase):
    def test_valid_comment_form(self):
        form = EventCommentForm(data={'content': 'Nice event!'})
        self.assertTrue(form.is_valid())

    def test_blank_comment_rejected(self):
        form = EventCommentForm(data={'content': ''})
        self.assertFalse(form.is_valid())
