from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from fruits.models import Fruit
from diseases.models import Disease

class UploadedImage(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='uploaded_images')
    image = models.ImageField(upload_to='uploads/%Y/%m/%d/')
    original_filename = models.CharField(max_length=255, blank=True, default='')
    file_size_bytes = models.PositiveIntegerField(default=0)
    width = models.PositiveIntegerField(default=0)
    height = models.PositiveIntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"Image #{self.id} ({self.original_filename or 'specimen'})"

    @property
    def file_size_display(self):
        if self.file_size_bytes < 1024:
            return f"{self.file_size_bytes} B"
        elif self.file_size_bytes < 1024 * 1024:
            return f"{self.file_size_bytes / 1024:.1f} KB"
        return f"{self.file_size_bytes / (1024 * 1024):.2f} MB"


class Prediction(models.Model):
    uploaded_image = models.OneToOneField(UploadedImage, on_delete=models.CASCADE, related_name='prediction')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='predictions')
    
    # ML Outputs
    fruit_name = models.CharField(max_length=100)
    disease_name = models.CharField(max_length=150)
    confidence = models.FloatField(help_text="Confidence percentage 0-100")
    is_mock = models.BooleanField(default=False, help_text="True if mock prediction service was utilized")
    model_source = models.CharField(max_length=150, default='CNN Classifier')

    # Optional relational link if matched in DB
    fruit_ref = models.ForeignKey(Fruit, on_delete=models.SET_NULL, null=True, blank=True)
    disease_ref = models.ForeignKey(Disease, on_delete=models.SET_NULL, null=True, blank=True)

    # Optional user inputs for enriched context
    temperature_input = models.CharField(max_length=50, blank=True, default='')
    humidity_input = models.CharField(max_length=50, blank=True, default='')
    user_notes = models.TextField(blank=True, default='')

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.fruit_name} - {self.disease_name} ({self.confidence:.1f}%)"

    @property
    def is_healthy(self):
        return 'healthy' in self.disease_name.lower() or (self.disease_ref and self.disease_ref.is_healthy)


class Diagnosis(models.Model):
    prediction = models.OneToOneField(Prediction, on_delete=models.CASCADE, related_name='diagnosis')
    severity = models.CharField(max_length=50, default='Moderate')
    pathogen = models.CharField(max_length=150, default='Unknown / Abiotic')
    
    symptoms_summary = models.TextField(blank=True, help_text="Comma-separated or JSON list of symptoms")
    environmental_factors_summary = models.TextField(blank=True)
    treatments_summary = models.TextField(blank=True)
    prevention_summary = models.TextField(blank=True)
    explanation = models.TextField(help_text="Detailed semantic ontology reasoning justification")

    ontology_individual = models.CharField(max_length=100, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Diagnosis for {self.prediction}"

    def get_symptoms_list(self):
        if not self.symptoms_summary:
            return []
        return [s.strip() for s in self.symptoms_summary.split(';') if s.strip()]

    def get_treatments_list(self):
        if not self.treatments_summary:
            return []
        return [t.strip() for t in self.treatments_summary.split(';') if t.strip()]

    def get_prevention_list(self):
        if not self.prevention_summary:
            return []
        return [p.strip() for p in self.prevention_summary.split(';') if p.strip()]

    def get_environmental_list(self):
        if not self.environmental_factors_summary:
            return []
        return [e.strip() for e in self.environmental_factors_summary.split(';') if e.strip()]
