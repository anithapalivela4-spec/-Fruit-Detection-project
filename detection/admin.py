from django.contrib import admin
from .models import UploadedImage, Prediction, Diagnosis

@admin.register(UploadedImage)
class UploadedImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'original_filename', 'user', 'file_size_display', 'uploaded_at')
    search_fields = ('original_filename', 'user__username')
    list_filter = ('uploaded_at',)

class DiagnosisInline(admin.StackedInline):
    model = Diagnosis
    extra = 0
    can_delete = False

@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'fruit_name', 'disease_name', 'confidence', 'is_mock', 'created_at')
    list_filter = ('fruit_name', 'is_mock', 'created_at')
    search_fields = ('fruit_name', 'disease_name', 'user__username')
    inlines = [DiagnosisInline]

@admin.register(Diagnosis)
class DiagnosisAdmin(admin.ModelAdmin):
    list_display = ('prediction', 'severity', 'pathogen', 'created_at')
    list_filter = ('severity',)
    search_fields = ('pathogen', 'explanation')
