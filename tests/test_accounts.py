from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from accounts.models import UserProfile

class AccountTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testfarmer',
            email='farmer@test.com',
            password='testpassword123'
        )

    def test_user_profile_creation(self):
        """Test UserProfile is automatically created via post_save signal."""
        self.assertTrue(hasattr(self.user, 'profile'))
        self.assertEqual(self.user.profile.role, 'farmer')
        self.assertFalse(self.user.profile.is_admin)

    def test_user_login(self):
        """Test successful authentication."""
        login_success = self.client.login(username='testfarmer', password='testpassword123')
        self.assertTrue(login_success)

    def test_user_registration_view(self):
        """Test registration endpoint creates user and profile."""
        response = self.client.post(reverse('accounts:register'), {
            'username': 'newuser',
            'email': 'new@test.com',
            'password': 'password123',
            'confirm_password': 'password123',
            'role': 'farmer',
            'farm_location': 'Nashik',
            'phone': '1234567890'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())
        user = User.objects.get(username='newuser')
        self.assertEqual(user.profile.farm_location, 'Nashik')

    def test_logout(self):
        """Test logout clears session."""
        self.client.login(username='testfarmer', password='testpassword123')
        response = self.client.get(reverse('accounts:logout'))
        self.assertEqual(response.status_code, 302)
