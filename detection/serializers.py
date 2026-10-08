from rest_framework import serializers
from fruits.models import Fruit
from diseases.models import Disease, Symptom, Treatment, Prevention
from detection.models import Prediction, Diagnosis

class FruitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fruit
        fields = ['id', 'fruit_name', 'scientific_name', 'variety', 'color', 'growth_stage', 'description', 'optimal_temperature', 'optimal_humidity', 'soil_type']


class SymptomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Symptom
        fields = ['id', 'name', 'visual_characteristics', 'affected_part', 'description']


class TreatmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Treatment
        fields = ['id', 'title', 'category', 'description', 'precautions', 'recommended_stage']


class PreventionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prevention
        fields = ['id', 'title', 'practice_type', 'description', 'season']


class DiseaseSerializer(serializers.ModelSerializer):
    fruit_name = serializers.CharField(source='affected_fruit.fruit_name', read_only=True)
    symptoms = SymptomSerializer(many=True, read_only=True)
    treatments = TreatmentSerializer(many=True, read_only=True)
    preventions = PreventionSerializer(many=True, read_only=True)

    class Meta:
        model = Disease
        fields = [
            'id', 'disease_name', 'code_name', 'fruit_name', 'is_healthy',
            'pathogen_name', 'severity', 'environmental_condition',
            'description', 'symptoms', 'treatments', 'preventions'
        ]


class DiagnosisSerializer(serializers.ModelSerializer):
    symptoms = serializers.SerializerMethodField()
    treatments = serializers.SerializerMethodField()
    prevention = serializers.SerializerMethodField()

    class Meta:
        model = Diagnosis
        fields = ['severity', 'pathogen', 'symptoms', 'treatments', 'prevention', 'explanation', 'ontology_individual']

    def get_symptoms(self, obj):
        return obj.get_symptoms_list()

    def get_treatments(self, obj):
        return obj.get_treatments_list()

    def get_prevention(self, obj):
        return obj.get_prevention_list()


class PredictionSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    image_url = serializers.SerializerMethodField()
    diagnosis = DiagnosisSerializer(read_only=True)

    class Meta:
        model = Prediction
        fields = [
            'id', 'username', 'fruit_name', 'disease_name', 'confidence',
            'is_mock', 'model_source', 'image_url', 'created_at', 'diagnosis'
        ]

    def get_image_url(self, obj):
        if obj.uploaded_image and obj.uploaded_image.image:
            return obj.uploaded_image.image.url
        return None
