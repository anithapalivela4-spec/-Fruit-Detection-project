from django import forms
from .models import Fruit

class FruitForm(forms.ModelForm):
    class Meta:
        model = Fruit
        fields = ['fruit_name', 'scientific_name', 'variety', 'color', 'growth_stage', 'description', 'optimal_temperature', 'optimal_humidity', 'soil_type', 'image']
        widgets = {
            'fruit_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Mango'}),
            'scientific_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Mangifera indica'}),
            'variety': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Alphonso, Kesar'}),
            'color': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Green to Golden Yellow'}),
            'growth_stage': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'optimal_temperature': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 24°C - 30°C'}),
            'optimal_humidity': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 50% - 65%'}),
            'soil_type': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Well-drained alluvial soil'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }
