import os
import io
import django
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image

from detection.models import Prediction
from fruits.models import Fruit
from diseases.models import Disease

class TenFruitTestCases(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Ensure test user
        cls.user = User.objects.create_user(username='testfarmer', password='password123')

        # Fruit & Disease ground truth definitions
        fruits_data = ['Banana', 'Apple', 'Tomato', 'Grape', 'Mango', 'Orange']
        cls.fruits = {}
        # Create Healthy Disease record
        for name in fruits_data:
            f, _ = Fruit.objects.get_or_create(fruit_name=name)
            cls.fruits[name] = f
            Disease.objects.get_or_create(
                disease_name=f"{name} Healthy",
                defaults={
                    "code_name": f"{name}___Healthy",
                    "affected_fruit": f,
                    "is_healthy": True,
                    "description": f"Specimen displays healthy {name} plant tissue with zero necrotic lesions."
                }
            )

        # Create Diseased records
        diseases_data = [
            ('Banana', 'Banana Sigatoka'),
            ('Apple', 'Apple Scab'),
            ('Tomato', 'Tomato Early Blight'),
            ('Grape', 'Grape Black Rot'),
            ('Mango', 'Mango Anthracnose'),
            ('Orange', 'Citrus Canker'),
        ]
        for f_name, d_name in diseases_data:
            Disease.objects.get_or_create(
                disease_name=d_name,
                defaults={
                    "code_name": d_name.replace(" ", "___"),
                    "affected_fruit": cls.fruits[f_name],
                    "is_healthy": False,
                    "description": f"{d_name} pathology affecting {f_name}."
                }
            )

    def setUp(self):
        self.client = Client()
        self.client.login(username='testfarmer', password='password123')

    def test_all_ten_cases_end_to_end(self):
        cases = [
            # 1. Healthy Banana
            {
                "case": "Healthy Banana",
                "path": "static/images/banana.png",
                "expected_fruit": "Banana",
                "expected_status": "Healthy",
                "expected_disease": "No disease detected",
                "is_healthy": True
            },
            # 2. Healthy Apple
            {
                "case": "Healthy Apple",
                "path": "static/images/apple.png",
                "expected_fruit": "Apple",
                "expected_status": "Healthy",
                "expected_disease": "No disease detected",
                "is_healthy": True
            },
            # 3. Healthy Tomato
            {
                "case": "Healthy Tomato",
                "path": "static/images/tomato.png",
                "expected_fruit": "Tomato",
                "expected_status": "Healthy",
                "expected_disease": "No disease detected",
                "is_healthy": True
            },
            # 4. Healthy Grape
            {
                "case": "Healthy Grape",
                "path": "static/images/grapes.png",
                "expected_fruit": "Grape",
                "expected_status": "Healthy",
                "expected_disease": "No disease detected",
                "is_healthy": True
            },
            # 5. Healthy Mango
            {
                "case": "Healthy Mango",
                "path": "static/images/mango.png",
                "expected_fruit": "Mango",
                "expected_status": "Healthy",
                "expected_disease": "No disease detected",
                "is_healthy": True
            },
            # 6. Diseased Banana
            {
                "case": "Diseased Banana",
                "path": "media/uploads/2026/10/08/Screenshot_2026-10-08_171653.png",
                "expected_fruit": "Banana",
                "expected_status": "Diseased",
                "expected_disease": "Banana Sigatoka",
                "is_healthy": False
            },
            # 7. Diseased Apple
            {
                "case": "Diseased Apple",
                "path": "media/uploads/2026/10/08/Screenshot_2026-10-08_171602.png",
                "expected_fruit": "Apple",
                "expected_status": "Diseased",
                "expected_disease": "Apple Scab",
                "is_healthy": False
            },
            # 8. Diseased Tomato
            {
                "case": "Diseased Tomato",
                "path": "media/uploads/2026/10/08/Screenshot_2026-10-08_171733.png",
                "expected_fruit": "Tomato",
                "expected_status": "Diseased",
                "expected_disease": "Tomato Early Blight",
                "is_healthy": False
            },
            # 9. Diseased Grape
            {
                "case": "Diseased Grape",
                "path": "media/uploads/2026/10/08/Screenshot_2026-10-08_171632.png",
                "expected_fruit": "Grape",
                "expected_status": "Diseased",
                "expected_disease": "Grape Black Rot",
                "is_healthy": False
            },
            # 10. Diseased Mango
            {
                "case": "Diseased Mango",
                "path": "media/uploads/2026/10/08/Screenshot_2026-10-08_142512.png",
                "expected_fruit": "Mango",
                "expected_status": "Diseased",
                "expected_disease": "Mango Anthracnose",
                "is_healthy": False
            },
        ]

        print("\n" + "=" * 80)
        print("   TESTING 10 SPECIMEN CASES: END-TO-END PREDICTION & RESULT PAGE")
        print("=" * 80)

        for c in cases:
            self.assertTrue(os.path.exists(c["path"]), f"Image not found: {c['path']}")
            with open(c["path"], "rb") as f:
                uploaded = SimpleUploadedFile(os.path.basename(c["path"]), f.read(), content_type="image/png")

            # POST to detection view
            response = self.client.post(reverse('detection:detect'), {
                'image': uploaded
            }, follow=True)

            self.assertEqual(response.status_code, 200)

            # Get the latest prediction
            pred = Prediction.objects.order_by('-created_at').first()
            self.assertIsNotNone(pred)

            # 1. Verify Fruit Name
            self.assertEqual(pred.fruit_name, c["expected_fruit"],
                             f"[{c['case']}] Wrong fruit: expected {c['expected_fruit']}, got {pred.fruit_name}")

            # 2. Verify Healthy / Diseased status
            self.assertEqual(pred.is_healthy, c["is_healthy"],
                             f"[{c['case']}] Wrong status: expected healthy={c['is_healthy']}, got {pred.is_healthy}")

            # 3. Verify Disease Name
            self.assertEqual(pred.disease_name, c["expected_disease"],
                             f"[{c['case']}] Wrong disease: expected {c['expected_disease']}, got {pred.disease_name}")

            # 4. Verify Result Page HTML Rendering
            html = response.content.decode('utf-8')

            # Fruit name displayed in attributes table
            self.assertIn(f">{pred.fruit_name}</span>", html)

            # Disease name displayed in attributes table
            self.assertIn(c['expected_disease'], html)

            # Status badge displayed
            if c["is_healthy"]:
                self.assertIn('result-badge-healthy">Healthy</span>', html)
                self.assertIn('Healthy Specimen Verified', html)
                # Confirm NO disease name shown for healthy
                self.assertNotIn('Apple Scab', html)
                self.assertNotIn('Banana Sigatoka', html)
                self.assertNotIn('Tomato Early Blight', html)
                self.assertNotIn('Grape Black Rot', html)
                self.assertNotIn('Mango Anthracnose', html)
            else:
                self.assertIn('result-badge-diseased">Diseased</span>', html)
                self.assertIn('Disease Detected', html)

            status_str = "Healthy" if pred.is_healthy else "Diseased"
            print(f"[PASS] {c['case']:18} -> Fruit: {pred.fruit_name:7} | Status: {status_str:8} | Disease: {pred.disease_name:22} | Confidence: {pred.confidence:.1f}%")

        print("=" * 80)
        print("ALL 10 TARGET CASES VERIFIED AND PASSED!")
        print("=" * 80 + "\n")
