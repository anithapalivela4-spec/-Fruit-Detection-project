from django.contrib import admin
from .models import Disease, Symptom, EnvironmentalFactor, Treatment, Prevention, Pathogen

@admin.register(Pathogen)
class PathogenAdmin(admin.ModelAdmin):
    list_display = ('name', 'pathogen_type', 'scientific_name')
    search_fields = ('name', 'scientific_name')

@admin.register(Symptom)
class SymptomAdmin(admin.ModelAdmin):
    list_display = ('name', 'affected_part', 'visual_characteristics')
    search_fields = ('name', 'description')

@admin.register(EnvironmentalFactor)
class EnvironmentalFactorAdmin(admin.ModelAdmin):
    list_display = ('name', 'temperature_range', 'humidity_range')

@admin.register(Treatment)
class TreatmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'recommended_stage')
    list_filter = ('category',)
    search_fields = ('title', 'description')

@admin.register(Prevention)
class PreventionAdmin(admin.ModelAdmin):
    list_display = ('title', 'practice_type', 'season')
    search_fields = ('title', 'description')

@admin.register(Disease)
class DiseaseAdmin(admin.ModelAdmin):
    list_display = ('disease_name', 'affected_fruit', 'severity', 'is_healthy', 'pathogen_name')
    list_filter = ('severity', 'is_healthy', 'affected_fruit')
    search_fields = ('disease_name', 'description', 'pathogen_name')
    filter_horizontal = ('symptoms', 'environmental_factors', 'treatments', 'preventions')
