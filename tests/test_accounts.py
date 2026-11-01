from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from accounts.models import UserProfile
from detection.models import Prediction, UploadedImage
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
import io

class AccountTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='existingfarmer',
            email='farmer@fruit.com',
            password='testpassword123',
            first_name='Ramesh',
            last_name='Kumar'
        )

    def test_registration_new_user(self):
        """Test registration creates user, hashes password, and redirects to login."""
        response = self.client.post(reverse('accounts:register'), {
            'full_name': 'Anitha Devi',
            'email': 'anitha@example.com',
            'password': 'securepassword123',
            'confirm_password': 'securepassword123',
        })
        # Must redirect to login page (not dashboard)
        self.assertRedirects(response, reverse('accounts:login'))

        # Check database persistence and password hashing
        user = User.objects.get(email='anitha@example.com')
        self.assertEqual(user.first_name, 'Anitha')
        self.assertEqual(user.last_name, 'Devi')
        self.assertTrue(user.check_password('securepassword123'))
        self.assertTrue(hasattr(user, 'profile'))

    def test_registration_duplicate_email(self):
        """Test duplicate email is rejected with error."""
        response = self.client.post(reverse('accounts:register'), {
            'full_name': 'Another Ramesh',
            'email': 'farmer@fruit.com',  # already exists
            'password': 'password123',
            'confirm_password': 'password123',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'An account with this email address already exists')

    def test_registration_mismatched_password(self):
        """Test password mismatch triggers validation error."""
        response = self.client.post(reverse('accounts:register'), {
            'full_name': 'Test User',
            'email': 'testuser@fruit.com',
            'password': 'password123',
            'confirm_password': 'differentpassword',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Passwords do not match')

    def test_login_with_email_success(self):
        """Test login using registered email and redirect to dashboard."""
        response = self.client.post(reverse('accounts:login'), {
            'email': 'farmer@fruit.com',
            'password': 'testpassword123'
        })
        self.assertRedirects(response, reverse('dashboard'))
        self.assertEqual(int(self.client.session['_auth_user_id']), self.user.pk)

    def test_login_incorrect_password(self):
        """Test login failure with wrong password displays error."""
        response = self.client.post(reverse('accounts:login'), {
            'email': 'farmer@fruit.com',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Invalid email or password')

    def test_logout_redirects_to_login(self):
        """Test logout clears session and redirects to login."""
        self.client.login(username='existingfarmer', password='testpassword123')
        response = self.client.get(reverse('accounts:logout'))
        self.assertRedirects(response, reverse('accounts:login'))
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_protected_routes_require_login(self):
        """Unauthenticated requests to Dashboard and History must redirect to login."""
        # Only Dashboard and History require authentication
        protected_urls = [
            reverse('dashboard'),
            reverse('detection:history'),
        ]
        for url in protected_urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302,
                             msg=f"{url} should redirect unauthenticated users to login")
            self.assertIn(reverse('accounts:login'), response.url)

    def test_public_detect_page_no_login_required(self):
        """Public pages must be accessible to all visitors without login (HTTP 200)."""
        public_urls = [
            reverse('detection:detect'),
            reverse('home'),
            reverse('about'),
            reverse('gallery'),
            reverse('contact'),
        ]
        for url in public_urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200,
                             msg=f"{url} should be publicly accessible without login")

    def test_user_history_isolation(self):
        """User A should not see User B's predictions in their history."""
        user_b = User.objects.create_user(
            username='user_b',
            email='user_b@fruit.com',
            password='password123'
        )

        # Create dummy image
        img = Image.new('RGB', (50, 50), color=(0, 255, 0))
        b = io.BytesIO()
        img.save(b, format='JPEG')
        f = SimpleUploadedFile('test.jpg', b.getvalue(), content_type='image/jpeg')

        up = UploadedImage.objects.create(user=user_b, image=f, original_filename='test.jpg')
        pred_b = Prediction.objects.create(
            uploaded_image=up,
            user=user_b,
            fruit_name='Mango',
            disease_name='Mango Anthracnose',
            confidence=95.0
        )

        # Log in as user A
        self.client.login(username='existingfarmer', password='testpassword123')
        hist_response = self.client.get(reverse('detection:history'))
        self.assertEqual(hist_response.status_code, 200)
        self.assertNotContains(hist_response, 'Mango Anthracnose')

        # User A attempting to view user B's result directly
        result_response = self.client.get(reverse('detection:result', args=[pred_b.id]))
        self.assertRedirects(result_response, reverse('detection:history'))
