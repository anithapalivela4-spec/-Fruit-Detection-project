from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth.models import User
from fruits.models import Fruit
from diseases.models import Disease
from detection.models import Prediction, UploadedImage, Diagnosis
from detection.serializers import FruitSerializer, DiseaseSerializer, PredictionSerializer
from detection.services.predictor import DetectionPredictorService
from detection.services.diagnosis import DiagnosisEngine
from ontology_engine.ontology_loader import OntologyLoader
from ontology_engine.reasoner import OntologyReasoner

class FruitListAPIView(APIView):
    def get(self, request):
        fruits = Fruit.objects.all()
        serializer = FruitSerializer(fruits, many=True)
        return Response(serializer.data)


class DiseaseListAPIView(APIView):
    def get(self, request):
        diseases = Disease.objects.all().select_related('affected_fruit').prefetch_related('symptoms', 'treatments', 'preventions')
        serializer = DiseaseSerializer(diseases, many=True)
        return Response(serializer.data)


class PredictAPIView(APIView):
    """
    POST: Upload image file (multipart/form-data) and receive immediate
    integrated ML + Ontology diagnosis response.
    """
    def post(self, request):
        if 'image' not in request.FILES:
            return Response({'error': 'No image file provided. Parameter key must be "image".'}, status=status.HTTP_400_BAD_REQUEST)

        image_file = request.FILES['image']
        fruit_hint = request.data.get('fruit_hint')

        # Use authenticated user or demo public user
        user = request.user if request.user.is_authenticated else User.objects.first()

        # Save uploaded image
        uploaded_img = UploadedImage.objects.create(
            user=user,
            image=image_file,
            original_filename=image_file.name,
            file_size_bytes=image_file.size
        )

        # Predict
        predictor = DetectionPredictorService()
        ml_res = predictor.run_prediction(uploaded_img.image.path, fruit_hint=fruit_hint)

        # Reason & diagnose
        diag_engine = DiagnosisEngine()
        diag_res = diag_engine.generate_diagnosis(ml_res)

        # Save Prediction & Diagnosis
        pred_obj = Prediction.objects.create(
            uploaded_image=uploaded_img,
            user=user,
            fruit_name=diag_res['fruit_name'],
            disease_name=diag_res['disease_name'],
            confidence=diag_res['confidence'],
            is_mock=diag_res['is_mock'],
            model_source=diag_res['model_source'],
            fruit_ref=diag_res['fruit_obj'],
            disease_ref=diag_res['disease_obj']
        )

        Diagnosis.objects.create(
            prediction=pred_obj,
            severity=diag_res['severity'],
            pathogen=diag_res['pathogen'],
            symptoms_summary="; ".join(diag_res['symptoms']),
            treatments_summary="; ".join(diag_res['treatments']),
            prevention_summary="; ".join(diag_res['prevention']),
            environmental_factors_summary="; ".join(diag_res['environmental_factors']),
            explanation=diag_res['explanation'],
            ontology_individual=diag_res.get('ontology_individual', '')
        )

        serializer = PredictionSerializer(pred_obj)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class HistoryAPIView(APIView):
    def get(self, request):
        if request.user.is_authenticated and not (request.user.is_superuser or getattr(request.user, 'profile', None) and request.user.profile.is_admin):
            predictions = Prediction.objects.filter(user=request.user)
        else:
            predictions = Prediction.objects.all()
        serializer = PredictionSerializer(predictions[:50], many=True)
        return Response(serializer.data)


class OntologyQueryAPIView(APIView):
    """
    Direct endpoint for semantic querying of FruitDiseaseOntology.
    Accepts query params: ?disease=Mango+Anthracnose or executes custom SPARQL queries.
    """
    def get(self, request):
        disease_name = request.GET.get('disease', 'Mango Anthracnose')
        reasoner = OntologyReasoner()
        reasoning_res = reasoner.reason({
            'fruit': request.GET.get('fruit', 'Mango'),
            'disease': disease_name,
            'confidence': 95.0
        })
        graph = OntologyLoader.get_graph()
        return Response({
            'ontology_name': 'FruitDiseaseOntology',
            'triple_count': len(graph),
            'disease_queried': disease_name,
            'reasoning_result': reasoning_res
        })
