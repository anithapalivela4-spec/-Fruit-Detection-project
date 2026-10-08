from django.db import models
from django.urls import reverse
from fruits.models import Fruit

class Pathogen(models.Model):
    PATHOGEN_TYPES = [
        ('fungal', 'Fungi / Fungal'),
        ('bacterial', 'Bacteria / Bacterial'),
        ('viral', 'Virus / Viral'),
        ('oomycete', 'Oomycete (Water Mold)'),
        ('none', 'None (Healthy / Abiotic)'),
    ]

    name = models.CharField(max_length=150)
    pathogen_type = models.CharField(max_length=30, choices=PATHOGEN_TYPES, default='fungal')
    scientific_name = models.CharField(max_length=150, blank=True, default='')
    characteristics = models.TextField(blank=True, default='')

    def __str__(self):
        return f"{self.name} ({self.get_pathogen_type_display()})"


class Symptom(models.Model):
    name = models.CharField(max_length=100, unique=True)
    visual_characteristics = models.CharField(max_length=200, blank=True, default='')
    description = models.TextField(blank=True, default='')
    affected_part = models.CharField(max_length=100, default='Leaves and Fruits')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class EnvironmentalFactor(models.Model):
    name = models.CharField(max_length=150, unique=True)
    temperature_range = models.CharField(max_length=50, blank=True, default='')
    humidity_range = models.CharField(max_length=50, blank=True, default='')
    description = models.TextField(blank=True, default='')

    def __str__(self):
        return self.name


class Treatment(models.Model):
    CATEGORY_CHOICES = [
        ('organic', 'Organic Treatment'),
        ('biological', 'Biological Treatment'),
        ('cultural', 'Cultural Treatment / Management'),
        ('chemical', 'General Chemical Guidance (Agricultural grade)'),
    ]

    title = models.CharField(max_length=150)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default='organic')
    description = models.TextField()
    precautions = models.TextField(blank=True, default='Wear protective gear. Do not exceed suggested dilution. Avoid spraying during high heat or bee activity.')
    recommended_stage = models.CharField(max_length=100, blank=True, default='At earliest symptom onset')

    def __str__(self):
        return f"[{self.get_category_display()}] {self.title}"


class Prevention(models.Model):
    title = models.CharField(max_length=150)
    practice_type = models.CharField(max_length=100, default='Sanitation & Field Hygiene')
    description = models.TextField()
    season = models.CharField(max_length=100, blank=True, default='Year-round / Pre-monsoon')

    def __str__(self):
        return f"{self.title} ({self.practice_type})"


class Disease(models.Model):
    SEVERITY_LEVELS = [
        ('healthy', 'None (Healthy)'),
        ('low', 'Low'),
        ('moderate', 'Moderate'),
        ('high', 'High'),
        ('critical', 'Critical / Severe'),
    ]

    disease_name = models.CharField(max_length=150, unique=True)
    code_name = models.CharField(max_length=100, unique=True, help_text="Dataset class key, e.g., Mango___Anthracnose")
    affected_fruit = models.ForeignKey(Fruit, on_delete=models.CASCADE, related_name='diseases')
    is_healthy = models.BooleanField(default=False)
    pathogen = models.ForeignKey(Pathogen, on_delete=models.SET_NULL, null=True, blank=True, related_name='diseases')
    pathogen_name = models.CharField(max_length=150, blank=True, default='')
    severity = models.CharField(max_length=20, choices=SEVERITY_LEVELS, default='moderate')
    environmental_condition = models.CharField(max_length=200, blank=True, default='')
    description = models.TextField()
    image = models.ImageField(upload_to='diseases/', blank=True, null=True)

    # Relationships
    symptoms = models.ManyToManyField(Symptom, blank=True, related_name='diseases')
    environmental_factors = models.ManyToManyField(EnvironmentalFactor, blank=True, related_name='diseases')
    treatments = models.ManyToManyField(Treatment, blank=True, related_name='diseases')
    preventions = models.ManyToManyField(Prevention, blank=True, related_name='diseases')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['affected_fruit__fruit_name', 'disease_name']

    def __str__(self):
        return f"{self.affected_fruit.fruit_name} - {self.disease_name}"

    def get_absolute_url(self):
        return reverse('diseases:disease_detail', kwargs={'pk': self.pk})
