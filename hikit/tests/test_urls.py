from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from hikit.models import Route, Event


class URLTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='pass')
        self.route = Route.objects.create(
            name='Sample Route',
            description='A beautiful path',
            distance=5.5,
            elevation_gain=300,
            difficulty='Easy',
            created_by=self.user
        )
        self.event = Event.objects.create(
            route=self.route,
            organizer=self.user,
            title='Morning Hike',
            description='Easy trail',
            date='2030-01-01T10:00:00Z',
            max_participants=10
        )

    def test_home_url(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_about_url(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)

    def test_route_list_url(self):
        response = self.client.get(reverse('route_list'))
        self.assertEqual(response.status_code, 200)

    def test_route_detail_url(self):
        response = self.client.get(reverse('route_detail', args=[self.route.id]))
        self.assertEqual(response.status_code, 200)

    def test_event_list_url(self):
        response = self.client.get(reverse('event_list'))
        self.assertEqual(response.status_code, 200)

    def test_event_detail_url(self):
        response = self.client.get(reverse('event_detail', args=[self.event.id]))
        self.assertEqual(response.status_code, 200)

    def test_profile_url_authenticated(self):
        self.client.login(username='testuser', password='pass')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)

    def test_profile_url_unauthenticated(self):
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_login_url(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_register_url(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_logout_url(self):
        self.client.login(username='testuser', password='pass')
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, 302)  # Should redirect
