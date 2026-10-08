from django.test import TestCase
import numpy as np
from PIL import Image
import io
from model.preprocessing.resize import resize_image
from model.preprocessing.normalization import normalize_image
from model.prediction.predict import FruitDiseasePredictor

class PredictionPipelineTests(TestCase):
    def setUp(self):
        # Create a test synthetic image in memory
        self.test_img = Image.new('RGB', (300, 300), color=(80, 160, 60))
        self.predictor = FruitDiseasePredictor()

    def test_resize_dimensions(self):
        """Test image resize outputs exact (224, 224)."""
        resized = resize_image(self.test_img, target_size=(224, 224))
        self.assertEqual(resized.size, (224, 224))

    def test_normalization_tensor(self):
        """Test normalization outputs float array in range [0, 1]."""
        resized = resize_image(self.test_img, target_size=(224, 224))
        normalized = normalize_image(resized, method='rescaling')
        self.assertEqual(normalized.shape, (1, 224, 224, 3))
        self.assertTrue(normalized.min() >= 0.0)
        self.assertTrue(normalized.max() <= 1.0)

    def test_mock_prediction_output_structure(self):
        """Test prediction returns structured dictionary with confidence and fruit."""
        res = self.predictor.predict(self.test_img, selected_fruit_hint='Mango')
        self.assertIn('fruit', res)
        self.assertIn('disease', res)
        self.assertIn('confidence', res)
        self.assertIsInstance(res['confidence'], float)
        self.assertGreaterEqual(res['confidence'], 0.0)
