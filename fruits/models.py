from django.db import models
from django.urls import reverse

class Variety(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, default='')

    class Meta:
        verbose_name_plural = 'Varieties'

    def __str__(self):
        return self.name


class Fruit(models.Model):
    GROWTH_STAGES = [
        ('flowering', 'Flowering Stage'),
        ('fruit_set', 'Fruit Set Stage'),
        ('development', 'Fruit Development Stage'),
        ('maturation', 'Maturation / Ripening Stage'),
        ('harvest', 'Harvest / Post-Harvest Stage'),
    ]

    fruit_name = models.CharField(max_length=100, unique=True)
    scientific_name = models.CharField(max_length=150, blank=True, default='')
    variety = models.CharField(max_length=150, blank=True, default='Standard Commercial Varieties')
    varieties = models.ManyToManyField(Variety, blank=True, related_name='fruits')
    color = models.CharField(max_length=60, blank=True, default='Green / Yellow / Red')
    growth_stage = models.CharField(max_length=30, choices=GROWTH_STAGES, default='development')
    description = models.TextField(blank=True, default='')
    image = models.ImageField(upload_to='fruits/', blank=True, null=True)
    optimal_temperature = models.CharField(max_length=50, blank=True, default='20°C - 30°C')
    optimal_humidity = models.CharField(max_length=50, blank=True, default='60% - 80%')
    soil_type = models.CharField(max_length=100, blank=True, default='Well-drained loamy soil')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['fruit_name']

    def __str__(self):
        return self.fruit_name

    def get_absolute_url(self):
        return reverse('fruits:fruit_detail', kwargs={'pk': self.pk})

    @property
    def total_diseases(self):
        return self.diseases.count()
