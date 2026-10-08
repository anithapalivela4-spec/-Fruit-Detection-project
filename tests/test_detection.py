from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
import io
from fruits.models import Fruit
from diseases.models import Disease
from detection.models import Prediction, UploadedImage, Diagnosis

class DetectionFlowTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='ramesh',
            password='password123'
        )
        self.client.login(username='ramesh', password='password123')
        
        self.fruit = Fruit.objects.create(
            fruit_name='Mango',
            scientific_name='Mangifera indica'
        )
        self.disease = Disease.objects.create(
            disease_name='Mango Anthracnose',
            code_name='Mango___Anthracnose',
            affected_fruit=self.fruit,
            severity='high',
            description='Fungal infection.'
        )

    def test_image_upload_and_detection(self):
        """Test full end-to-end detection pipeline from upload to result."""
        # Create test in-memory image
        img = Image.new('RGB', (100, 100), color=(50, 120, 40))
        buf = io.BytesIO()
        img.save(buf, format='JPEG')
        uploaded = SimpleUploadedFile("leaf.jpg", buf.getvalue(), content_type="image/jpeg")

        response = self.client.post(reverse('detection:detect'), {
            'image': uploaded,
            'fruit_hint': 'Mango',
            'temperature': '28',
            'humidity': '80'
        })
        self.assertEqual(response.status_code, 302)
        
        # Verify prediction created in database
        self.assertEqual(Prediction.objects.count(), 1)
        pred = Prediction.objects.first()
        self.assertEqual(pred.user, self.user)
        self.assertTrue(hasattr(pred, 'diagnosis'))
        self.assertIsNotNone(pred.diagnosis.severity)

    def test_history_isolation(self):
        """Test that regular users only see their own predictions in history."""
        # Create another user and prediction
        other_user = User.objects.create_user(username='other', password='pass')
        up_img = UploadedImage.objects.create(user=other_user)
        Prediction.objects.create(
            uploaded_image=up_img,
            user=other_user,
            fruit_name='Apple',
            disease_name='Apple Scab',
            confidence=92.0
        )

        response = self.client.get(reverse('detection:history'))
        self.assertEqual(response.status_code, 200)
        # Other user's prediction should NOT be in context
        predictions_in_page = response.context['page_obj'].object_list
        for p in predictions_in_page:
            self.assertEqual(p.user, self.user)
