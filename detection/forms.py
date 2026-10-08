from django import forms
from .services.image_processor import validate_uploaded_image
from fruits.models import Fruit

class ImageUploadForm(forms.Form):
    image = forms.ImageField(
        label="Select Leaf / Fruit Specimen Image",
        widget=forms.FileInput(attrs={
            'class': 'form-control form-control-lg',
            'id': 'image-file-input',
            'accept': 'image/jpeg,image/png,image/webp,image/jpg'
        })
    )
    fruit_hint = forms.ChoiceField(
        required=False,
        label="Target Fruit (Optional)",
        choices=[
            ('', '-- Auto-Detect Fruit from Specimen --'),
            ('Mango', 'Mango'),
            ('Apple', 'Apple'),
            ('Grape', 'Grape'),
            ('Orange', 'Orange / Citrus'),
            ('Banana', 'Banana'),
            ('Guava', 'Guava'),
            ('Papaya', 'Papaya'),
            ('Tomato', 'Tomato'),
            ('Pomegranate', 'Pomegranate'),
        ],
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    temperature = forms.CharField(
        required=False,
        label="Ambient Temperature (°C)",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 28'})
    )
    humidity = forms.CharField(
        required=False,
        label="Relative Humidity (%)",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 75'})
    )
    user_notes = forms.CharField(
        required=False,
        label="Field Observation Notes",
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Optional observations (e.g. onset 3 days ago, lower canopy)'})
    )

    def clean_image(self):
        img = self.cleaned_data.get('image')
        if img:
            validate_uploaded_image(img)
        return img
