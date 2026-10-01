from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Event, Registration
from django.utils import timezone

class EventRegistrationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.event = Event.objects.create(
            title='Test Event',
            description='Test Description',
            date=timezone.now(),
            location='Test Location',
            capacity=1
        )
        self.register_url = reverse('register_event', args=[self.event.pk])
        self.cancel_url = reverse('cancel_registration', args=[self.event.pk])
        self.dashboard_url = reverse('dashboard')

    def test_access_control_unauthenticated(self):
        """Unauthenticated users should be redirected to login for protected routes."""
        # Try to register
        response = self.client.post(self.register_url)
        self.assertRedirects(response, f"/login/?next={self.register_url}")

        # Try to view dashboard
        response = self.client.get(self.dashboard_url)
        self.assertRedirects(response, f"/login/?next={self.dashboard_url}")

    def test_successful_registration(self):
        """Authenticated user should be able to register."""
        self.client.login(username='testuser', password='password123')
        response = self.client.post(self.register_url)
        
        # Should redirect to dashboard
        self.assertRedirects(response, self.dashboard_url)
        self.assertTrue(Registration.objects.filter(user=self.user, event=self.event).exists())
        self.assertEqual(self.event.available_seats(), 0)

    def test_duplicate_registration_prevention(self):
        """User cannot register for the same event twice."""
        # Register first time
        Registration.objects.create(user=self.user, event=self.event)
        
        # Try to register again
        self.client.login(username='testuser', password='password123')
        response = self.client.post(self.register_url)
        
        # Should redirect back to event detail
        self.assertRedirects(response, reverse('event_detail', args=[self.event.pk]))
        # Total registrations should still be 1
        self.assertEqual(Registration.objects.filter(user=self.user, event=self.event).count(), 1)

    def test_capacity_limits(self):
        """Cannot register if event is full."""
        # Create another user and register them to fill capacity
        other_user = User.objects.create_user(username='other', password='password123')
        Registration.objects.create(user=other_user, event=self.event)
        
        # Event should be full
        self.assertTrue(self.event.is_full())
        
        # Try to register with testuser
        self.client.login(username='testuser', password='password123')
        response = self.client.post(self.register_url)
        
        # Should redirect to event detail
        self.assertRedirects(response, reverse('event_detail', args=[self.event.pk]))
        self.assertFalse(Registration.objects.filter(user=self.user, event=self.event).exists())

    def test_cancel_registration(self):
        """User can cancel their registration."""
        Registration.objects.create(user=self.user, event=self.event)
        
        self.client.login(username='testuser', password='password123')
        response = self.client.post(self.cancel_url)
        
        self.assertRedirects(response, self.dashboard_url)
        self.assertFalse(Registration.objects.filter(user=self.user, event=self.event).exists())
        self.assertEqual(self.event.available_seats(), 1)
