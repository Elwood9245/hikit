from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from hikit.models import Event, Route
from django.utils import timezone
from datetime import timedelta


class EventDetailViewTests(TestCase):
    def setUp(self):
        # Create test user and log in
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client = Client()
        self.client.login(username='testuser', password='password')

        # Create a route
        self.route = Route.objects.create(
            name="Test Route",
            description="Test description",
            distance=5.0,
            elevation_gain=200,
            difficulty="Easy",
            created_by=self.user
        )

        # Create an event
        self.event = Event.objects.create(
            route=self.route,
            organizer=self.user,
            title="Test Event",
            description="Test event description",
            date=timezone.now() + timedelta(days=7),
            max_participants=10
        )

    def test_event_detail_view_authenticated(self):
        response = self.client.get(reverse('event_detail', args=[self.event.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Event")
        self.assertContains(response, self.event.description)

    def test_event_detail_view_unauthenticated(self):
        self.client.logout()
        response = self.client.get(reverse('event_detail', args=[self.event.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Event")

    def test_post_comment_authenticated(self):
        response = self.client.post(reverse('event_detail', args=[self.event.id]), {
            'content': 'This is a test comment.'
        }, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        self.assertIn('Comment posted!', data['message'])
        self.assertIn('This is a test comment.', data['comment_html'])
        self.assertIn(self.user.username, data['comment_html'])

    def test_post_comment_unauthenticated(self):
        self.client.logout()
        response = self.client.post(reverse('event_detail', args=[self.event.id]), {
            'content': 'Unauthorized comment.'
        }, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(response.status_code, 200)  # Might be a redirect
        self.assertNotIn('Comment posted!', response.content.decode())


class RouteCreateViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='creator', password='testpass123')
        self.create_url = reverse('add_route')  # Update with your actual URL name

    def test_authenticated_user_can_create_route(self):
        self.client.login(username='creator', password='testpass123')
        response = self.client.post(self.create_url, {
            'name': 'Ben Nevis Trail',
            'description': 'Challenging and scenic route',
            'distance': 10.5,
            'elevation_gain': 1350,
            'difficulty': 'Hard',
        })
        self.assertEqual(response.status_code, 302)  # Redirect after creation
        self.assertEqual(Route.objects.count(), 1)
        self.assertEqual(Route.objects.first().name, 'Ben Nevis Trail')
        self.assertEqual(Route.objects.first().created_by, self.user)

    def test_unauthenticated_user_cannot_create_route(self):
        response = self.client.post(self.create_url, {
            'name': 'Unauthorized Route',
            'description': 'Should not be created',
            'distance': 5.0,
            'elevation_gain': 500,
            'difficulty': 'Medium',
        })
        self.assertEqual(response.status_code, 302)  # Should redirect to login
        self.assertEqual(Route.objects.count(), 0)


class AdditionalViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='tester', password='testpass123')
        self.route = Route.objects.create(
            name='Sample Route',
            description='Great hike!',
            distance=10,
            elevation_gain=200,
            difficulty='Easy',
            created_by=self.user
        )
        self.event = Event.objects.create(
            route=self.route,
            organizer=self.user,
            title="Sample Event",
            description="Event desc",
            date="2025-12-12T10:00:00Z",
            max_participants=10
        )

    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.route.id)

    def test_about_view(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)

    def test_route_list_view(self):
        response = self.client.get(reverse('route_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.route.name)

    def test_add_route_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('add_route'))
        self.assertEqual(response.status_code, 302)  # Should redirect to login

    def test_event_list_view(self):
        response = self.client.get(reverse('event_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.event.title)

    def test_search_view(self):
        response = self.client.get(reverse('search') + '?q=Sample')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.route.name)

    def test_toggle_save_route_authenticated(self):
        self.client.login(username='tester', password='testpass123')
        response = self.client.post(reverse('toggle_save_route', args=[self.route.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.route.saved_by.filter(id=self.user.id).exists())

    def test_toggle_save_route_unauthenticated(self):
        response = self.client.post(reverse('toggle_save_route', args=[self.route.id]))
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_profile_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 302)

    def test_profile_view_logged_in(self):
        self.client.login(username='tester', password='testpass123')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)