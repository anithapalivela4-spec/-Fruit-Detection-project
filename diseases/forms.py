from django import forms
from .models import Disease, Symptom, Treatment, Prevention, EnvironmentalFactor

class DiseaseForm(forms.ModelForm):
    class Meta:
        model = Disease
        fields = [
            'disease_name', 'code_name', 'affected_fruit', 'is_healthy',
            'pathogen_name', 'severity', 'environmental_condition',
            'description', 'image', 'symptoms', 'environmental_factors',
            'treatments', 'preventions'
        ]
        widgets = {
            'disease_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Apple Scab'}),
            'code_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Apple___Scab'}),
            'affected_fruit': forms.Select(attrs={'class': 'form-select'}),
            'is_healthy': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'pathogen_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Venturia inaequalis (Fungus)'}),
            'severity': forms.Select(attrs={'class': 'form-select'}),
            'environmental_condition': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Cool, wet spring weather (17°C - 24°C)'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'symptoms': forms.SelectMultiple(attrs={'class': 'form-select', 'size': 6}),
            'environmental_factors': forms.SelectMultiple(attrs={'class': 'form-select', 'size': 4}),
            'treatments': forms.SelectMultiple(attrs={'class': 'form-select', 'size': 5}),
            'preventions': forms.SelectMultiple(attrs={'class': 'form-select', 'size': 5}),
        }


class SymptomForm(forms.ModelForm):
    class Meta:
        model = Symptom
        fields = ['name', 'visual_characteristics', 'description', 'affected_part']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Black Spot'}),
            'visual_characteristics': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'affected_part': forms.TextInput(attrs={'class': 'form-control'}),
        }


class TreatmentForm(forms.ModelForm):
    class Meta:
        model = Treatment
        fields = ['title', 'category', 'description', 'precautions', 'recommended_stage']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'precautions': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'recommended_stage': forms.TextInput(attrs={'class': 'form-control'}),
        }


class PreventionForm(forms.ModelForm):
    class Meta:
        model = Prevention
        fields = ['title', 'practice_type', 'description', 'season']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'practice_type': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'season': forms.TextInput(attrs={'class': 'form-control'}),
        }
