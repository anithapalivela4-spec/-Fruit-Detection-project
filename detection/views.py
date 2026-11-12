import os
import csv
import json
from django.core.files import File
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.db.models import Count, Q
from django.core.paginator import Paginator

from .forms import ImageUploadForm
from .models import UploadedImage, Prediction, Diagnosis
from .services.image_processor import process_specimen_image
from .services.predictor import DetectionPredictorService
from .services.diagnosis import DiagnosisEngine
from reports.report_generator import generate_text_report
from fruits.models import Fruit
from diseases.models import Disease, Symptom, Treatment, Prevention
from django.contrib.auth.models import User


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['fruits_count'] = Fruit.objects.count()
        ctx['diseases_count'] = Disease.objects.count()
        ctx['predictions_count'] = Prediction.objects.count()
        ctx['featured_fruits'] = Fruit.objects.all()[:6]
        ctx['featured_diseases'] = Disease.objects.filter(is_healthy=False)[:6]
        return ctx


class AboutView(TemplateView):
    template_name = 'about.html'


class ContactView(View):
    def get(self, request):
        return render(request, 'contact.html')

    def post(self, request):
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        message = request.POST.get('message', '').strip()
        messages.success(request, f"Thank you {name or 'for reaching out'}! Your message has been sent successfully. Our agronomy team will get back to you shortly.")
        return render(request, 'contact.html', {'success': True})


DISEASE_IMAGE_MAP = {
    'Apple Black Rot': '/static/images/gallery/apple_black_rot.png',
    'Apple Scab': '/static/images/gallery/apple_scab.png',
    'Apple Healthy': '/static/images/gallery/apple_healthy.png',
    'Banana Sigatoka': '/static/images/gallery/banana_sigatoka.png',
    'Banana Healthy': '/static/images/gallery/banana_healthy.png',
    'Grape Black Rot': '/static/images/gallery/grape_black_rot.png',
    'Grape Healthy': '/static/images/gallery/grape_healthy.png',
    'Mango Anthracnose': '/static/images/gallery/mango_anthracnose.png',
    'Mango Powdery Mildew': '/static/images/gallery/mango_powdery_mildew.png',
    'Mango Healthy': '/static/images/gallery/mango_healthy.png',
    'Citrus Canker': '/static/images/gallery/citrus_canker.png',
    'Orange Healthy': '/static/images/gallery/orange_healthy.png',
    'Tomato Early Blight': '/static/images/gallery/tomato_early_blight.png',
    'Tomato Healthy': '/static/images/gallery/tomato_healthy.png',
    'Guava Healthy': '/static/images/gallery/guava_healthy.png',
    'Guava Wilt': '/static/images/gallery/guava_wilt.png',
    'Papaya Healthy': '/static/images/gallery/papaya_healthy.png',
    'Papaya Ringspot': '/static/images/gallery/papaya_ringspot.png',
    'Pomegranate Healthy': '/static/images/gallery/pomegranate_healthy.png',
    'Pomegranate Bacterial Blight': '/static/images/gallery/pomegranate_bacterial_blight.png',
}

ADDITIONAL_SPECIMENS = [
    {
        'title': 'Green Apple Variety (Granny Smith)',
        'fruit': 'Apple',
        'is_healthy': True,
        'image': '/static/images/gallery/apple_green_healthy.png',
        'tag': 'Cultivar Specimen',
        'description': 'Crisp emerald green apple with uniform glossy skin and zero foliar or fruit blemish.'
    },
    {
        'title': 'Red Apple Cluster on Branch',
        'fruit': 'Apple',
        'is_healthy': True,
        'image': '/static/images/gallery/apple_red_cluster.png',
        'tag': 'Orchard Cluster',
        'description': 'Sun-ripened red apple cluster growing in temperate orchard showing optimal healthy maturity.'
    },
    {
        'title': 'Red Gala Harvest Apple',
        'fruit': 'Apple',
        'is_healthy': True,
        'image': '/static/images/gallery/apple_red_crisp.png',
        'tag': 'Market Grade',
        'description': 'Grade-A red apple specimen with natural wax bloom and clean stem cavity.'
    },
    {
        'title': 'Field Banana Bunch on Plantation Tree',
        'fruit': 'Banana',
        'is_healthy': True,
        'image': '/static/images/gallery/banana_field_bunch.png',
        'tag': 'Plantation Specimen',
        'description': 'Full healthy green banana bunch hanging from pseudo-stem under tropical canopy.'
    },
    {
        'title': 'Naturally Ripened Spotted Banana',
        'fruit': 'Banana',
        'is_healthy': True,
        'image': '/static/images/gallery/banana_ripe_spotted.png',
        'tag': 'Ripening Stage',
        'description': 'Natural physiological sugar spotting during maturation, distinct from fungal Sigatoka lesions.'
    },
    {
        'title': 'Commercial Yellow Banana Finger',
        'fruit': 'Banana',
        'is_healthy': True,
        'image': '/static/images/gallery/banana_market_specimen.png',
        'tag': 'Market Grade',
        'description': 'Unblemished yellow Cavendish banana specimen with uniform yellow peel.'
    },
    {
        'title': 'Single Curved Table Banana',
        'fruit': 'Banana',
        'is_healthy': True,
        'image': '/static/images/gallery/banana_single_curved.png',
        'tag': 'Morphological Standard',
        'description': 'Typical elongated single curved body used in geometric contour verification.'
    },
    {
        'title': 'Green Table Grape Cluster',
        'fruit': 'Grape',
        'is_healthy': True,
        'image': '/static/images/gallery/grape_green_cluster.png',
        'tag': 'Vineyard Specimen',
        'description': 'Tight cluster of translucent green Thompson seedless berries with crisp intact skin.'
    },
    {
        'title': 'Ripe Purple Grape Bunch',
        'fruit': 'Grape',
        'is_healthy': True,
        'image': '/static/images/gallery/grape_purple_healthy.png',
        'tag': 'Vineyard Harvest',
        'description': 'Lush dark purple grape berries coated in natural protective yeast bloom.'
    },
    {
        'title': 'Fresh Table Grape Specimen',
        'fruit': 'Grape',
        'is_healthy': True,
        'image': '/static/images/gallery/grape_table_variety.png',
        'tag': 'Market Grade',
        'description': 'Healthy bunch of plump table grapes free from mildew, botrytis, or black rot.'
    },
    {
        'title': 'Raw Green Mango Specimen',
        'fruit': 'Mango',
        'is_healthy': True,
        'image': '/static/images/gallery/mango_raw_healthy.png',
        'tag': 'Unripe Specimen',
        'description': 'Developing raw green mango with firm pericarp, free from anthracnose tear-stains.'
    },
    {
        'title': 'Tree-Ripened Golden Mango',
        'fruit': 'Mango',
        'is_healthy': True,
        'image': '/static/images/gallery/mango_ripe_specimen.png',
        'tag': 'Ripe Specimen',
        'description': 'Fully ripe golden Alphonso/Kesar mango exhibiting vibrant orange-yellow hue.'
    },
    {
        'title': 'Citrus Orchard Tree & Foliage',
        'fruit': 'Orange',
        'is_healthy': True,
        'image': '/static/images/gallery/orange_orchard_tree.png',
        'tag': 'Orchard Canopy',
        'description': 'Vigorous citrus tree bearing multiple healthy oranges with dark glossy foliage.'
    },
    {
        'title': 'Ripe Sweet Citrus Orange',
        'fruit': 'Orange',
        'is_healthy': True,
        'image': '/static/images/gallery/orange_citrus_ripe.png',
        'tag': 'Market Grade',
        'description': 'Golden-orange citrus specimen with smooth oil glands and zero bacterial canker halos.'
    },
    {
        'title': 'Single Navel Orange Specimen',
        'fruit': 'Orange',
        'is_healthy': True,
        'image': '/static/images/gallery/orange_navel_single.png',
        'tag': 'Harvest Grade',
        'description': 'Hand-picked navel orange with intact calyx button and vibrant rind.'
    },
    {
        'title': 'Fresh Tomatoes Ripening on Vine',
        'fruit': 'Tomato',
        'is_healthy': True,
        'image': '/static/images/gallery/tomato_vine_fresh.png',
        'tag': 'Greenhouse Specimen',
        'description': 'Vibrant truss of cluster tomatoes on healthy green calyx and vine.'
    },
    {
        'title': 'Field Harvest Salad Tomato',
        'fruit': 'Tomato',
        'is_healthy': True,
        'image': '/static/images/gallery/tomato_field_harvest.png',
        'tag': 'Field Specimen',
        'description': 'Plump red salad tomato showing uniform lycopene coloration and clean epidermis.'
    },
    {
        'title': 'Single Round Tomato Specimen',
        'fruit': 'Tomato',
        'is_healthy': True,
        'image': '/static/images/gallery/tomato_salad_round.png',
        'tag': 'Market Grade',
        'description': 'Firm greenhouse-grown round tomato with smooth skin and no blight lesions.'
    },
    {
        'title': 'Foliar Necrotic Leaf Spot Pathology',
        'fruit': 'Tomato',
        'is_healthy': False,
        'image': '/static/images/gallery/foliar_disease_leaf_spot.png',
        'tag': 'Pathological Marker',
        'description': 'Characteristic foliar necrotic leaf spots displaying concentric fungal rings and yellow halos.'
    },
]


class GalleryView(View):
    def get(self, request):
        fruits = Fruit.objects.all().prefetch_related('diseases')
        diseases = list(Disease.objects.all().select_related('affected_fruit'))
        for d in diseases:
            if d.image:
                d.gallery_image_url = d.image.url
            else:
                d.gallery_image_url = DISEASE_IMAGE_MAP.get(
                    d.disease_name,
                    '/static/images/hero-fruits.jpg'
                )

        total_images_count = len(diseases) + len(ADDITIONAL_SPECIMENS)

        context = {
            'fruits': fruits,
            'diseases': diseases,
            'additional_specimens': ADDITIONAL_SPECIMENS,
            'total_images_count': total_images_count,
        }
        return render(request, 'gallery.html', context)


@method_decorator(login_required, name='dispatch')
class DashboardView(View):
    def get(self, request):
        user = request.user
        predictions = Prediction.objects.filter(user=user).select_related('diagnosis', 'uploaded_image')

        total_predictions = predictions.count()
        healthy_results = predictions.filter(Q(disease_name__icontains='healthy') | Q(disease_name__icontains='no disease')).count()
        diseases_detected = total_predictions - healthy_results

        recent_predictions = predictions[:6]

        # Disease frequency distribution for Chart.js
        disease_counts = {}
        for p in predictions:
            d_name = p.disease_name
            disease_counts[d_name] = disease_counts.get(d_name, 0) + 1

        chart_labels = list(disease_counts.keys())[:7]
        chart_data = [disease_counts[k] for k in chart_labels]

        context = {
            'total_predictions': total_predictions,
            'diseases_detected': diseases_detected,
            'healthy_results': healthy_results,
            'recent_predictions': recent_predictions,
            'chart_labels': json.dumps(chart_labels),
            'chart_data': json.dumps(chart_data),
        }
        return render(request, 'dashboard.html', context)


@method_decorator(login_required, name='dispatch')
class AdminDashboardView(View):
    def get(self, request):
        if not (request.user.is_superuser or request.user.profile.is_admin):
            messages.error(request, "Access restricted to system administrators.")
            return redirect('dashboard')

        total_users = User.objects.count()
        total_fruits = Fruit.objects.count()
        total_diseases = Disease.objects.count()
        total_predictions = Prediction.objects.count()

        recent_predictions = Prediction.objects.all().select_related('user', 'uploaded_image', 'diagnosis')[:10]
        recent_users = User.objects.all().order_by('-date_joined')[:6]

        # Fruit breakdown for Chart.js
        fruit_data_qs = Prediction.objects.values('fruit_name').annotate(count=Count('fruit_name')).order_by('-count')[:6]
        fruit_chart_labels = [item['fruit_name'] for item in fruit_data_qs]
        fruit_chart_counts = [item['count'] for item in fruit_data_qs]

        context = {
            'total_users': total_users,
            'total_fruits': total_fruits,
            'total_diseases': total_diseases,
            'total_predictions': total_predictions,
            'recent_predictions': recent_predictions,
            'recent_users': recent_users,
            'fruit_chart_labels': json.dumps(fruit_chart_labels),
            'fruit_chart_counts': json.dumps(fruit_chart_counts),
        }
        return render(request, 'admin_dashboard.html', context)


class UploadAndDetectView(View):
    def get(self, request):
        form = ImageUploadForm()
        fruits = Fruit.objects.all()
        return render(request, 'upload.html', {'form': form, 'fruits': fruits})

    def post(self, request):
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image_file = form.cleaned_data['image']
            fruit_hint = form.cleaned_data.get('fruit_hint')
            temperature = form.cleaned_data.get('temperature', '').strip()
            humidity = form.cleaned_data.get('humidity', '').strip()
            user_notes = form.cleaned_data.get('user_notes', '').strip()

            # Support anonymous visitors (user=None if not logged in)
            active_user = request.user if request.user.is_authenticated else None

            # 1. Save uploaded image
            uploaded_img_obj = UploadedImage.objects.create(
                user=active_user,
                image=image_file,
                original_filename=image_file.name,
                file_size_bytes=image_file.size
            )

            # Extract image dimensions
            try:
                meta = process_specimen_image(uploaded_img_obj.image.path)
                uploaded_img_obj.width = meta['width']
                uploaded_img_obj.height = meta['height']
                uploaded_img_obj.save()
            except Exception:
                pass

            # 2. Run Deep Learning / Predictor pipeline
            predictor_service = DetectionPredictorService()
            ml_result = predictor_service.run_prediction(uploaded_img_obj.image.path, fruit_hint=fruit_hint)

            if ml_result.get('unsupported'):
                messages.warning(
                    request,
                    ml_result.get('message', "The uploaded image could not be identified as a supported fruit or disease specimen. Please upload a clear photo of Tomato, Orange, Grape, Apple, Mango, or Banana.")
                )
                return redirect('detection:detect')

            # 3. Run Semantic Ontology Reasoning Engine & Diagnostic Synthesis
            diag_engine = DiagnosisEngine()
            env_context = {
                'temperature': temperature,
                'humidity': humidity
            }
            diag_result = diag_engine.generate_diagnosis(ml_result, env_context=env_context)

            # 4. Persist Prediction record
            prediction_record = Prediction.objects.create(
                uploaded_image=uploaded_img_obj,
                user=active_user,
                fruit_name=diag_result['fruit_name'],
                disease_name=diag_result['disease_name'],
                confidence=diag_result['confidence'],
                is_mock=diag_result['is_mock'],
                model_source=diag_result['model_source'],
                fruit_ref=diag_result['fruit_obj'],
                disease_ref=diag_result['disease_obj'],
                temperature_input=temperature,
                humidity_input=humidity,
                user_notes=user_notes
            )

            # 5. Persist Diagnosis record
            Diagnosis.objects.create(
                prediction=prediction_record,
                severity=diag_result['severity'],
                pathogen=diag_result['pathogen'],
                symptoms_summary="; ".join(diag_result['symptoms']),
                environmental_factors_summary="; ".join(diag_result['environmental_factors']),
                treatments_summary="; ".join(diag_result['treatments']),
                prevention_summary="; ".join(diag_result['prevention']),
                explanation=diag_result['explanation'],
                ontology_individual=diag_result.get('ontology_individual', '')
            )

            if prediction_record.is_healthy:
                messages.success(request, f"Image processed successfully: Healthy {prediction_record.fruit_name} verified (No disease detected).")
            else:
                messages.success(request, f"Image processed successfully: {prediction_record.disease_name} detected.")
            return redirect('detection:result', pk=prediction_record.pk)

        fruits = Fruit.objects.all()
        return render(request, 'upload.html', {'form': form, 'fruits': fruits})




class ResultView(View):
    def get(self, request, pk):
        prediction = get_object_or_404(
            Prediction.objects.select_related('uploaded_image', 'user', 'diagnosis', 'fruit_ref', 'disease_ref'),
            pk=pk
        )
        # Allow: anonymous predictions (user=None), the prediction owner, or admins
        is_owner = (prediction.user is None) or (request.user.is_authenticated and prediction.user == request.user)
        is_admin = request.user.is_authenticated and (
            request.user.is_superuser or
            (hasattr(request.user, 'profile') and request.user.profile.is_admin)
        )
        if not (is_owner or is_admin):
            messages.error(request, "Permission denied. You can only view your own prediction records.")
            return redirect('detection:history')
        return render(request, 'result.html', {'prediction': prediction, 'diagnosis': getattr(prediction, 'diagnosis', None)})


@method_decorator(login_required, name='dispatch')
class HistoryView(View):
    def get(self, request):
        user = request.user
        query = request.GET.get('q', '').strip()
        fruit_filter = request.GET.get('fruit', '').strip()

        # Normal users see only their own history; admins see all
        if user.is_superuser or user.profile.is_admin:
            predictions = Prediction.objects.all()
            is_admin_view = True
        else:
            predictions = Prediction.objects.filter(user=user)
            is_admin_view = False

        if query:
            predictions = predictions.filter(
                Q(disease_name__icontains=query) | Q(fruit_name__icontains=query)
            )
        if fruit_filter:
            predictions = predictions.filter(fruit_name__iexact=fruit_filter)

        predictions = predictions.select_related('uploaded_image', 'user', 'diagnosis')

        paginator = Paginator(predictions, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        fruits = Fruit.objects.all()
        context = {
            'page_obj': page_obj,
            'is_admin_view': is_admin_view,
            'fruits': fruits,
            'query': query,
            'fruit_filter': fruit_filter,
            'total_count': predictions.count()
        }
        return render(request, 'history.html', context)


@method_decorator(login_required, name='dispatch')
class DeletePredictionView(View):
    def post(self, request, pk):
        prediction = get_object_or_404(Prediction, pk=pk)
        if not (request.user.is_superuser or request.user.profile.is_admin or prediction.user == request.user):
            messages.error(request, "Permission denied.")
            return redirect('detection:history')

        # Remove image file from media storage
        if prediction.uploaded_image and prediction.uploaded_image.image:
            try:
                if os.path.exists(prediction.uploaded_image.image.path):
                    os.remove(prediction.uploaded_image.image.path)
            except Exception:
                pass

        prediction.delete()
        messages.success(request, "Prediction record removed successfully.")
        return redirect('detection:history')


class ExportReportView(View):
    def get(self, request, pk):
        prediction = get_object_or_404(
            Prediction.objects.select_related('uploaded_image', 'user', 'diagnosis'),
            pk=pk
        )
        # Allow anonymous predictions or the authenticated owner/admin
        is_owner = (prediction.user is None) or (request.user.is_authenticated and prediction.user == request.user)
        is_admin = request.user.is_authenticated and (
            request.user.is_superuser or
            (hasattr(request.user, 'profile') and request.user.profile.is_admin)
        )
        if not (is_owner or is_admin):
            messages.error(request, "Permission denied.")
            return redirect('home')

        report_content = generate_text_report(prediction)
        response = HttpResponse(report_content, content_type='text/plain; charset=utf-8')
        response['Content-Disposition'] = f'attachment; filename="FruitDisease_Report_{prediction.id}.txt"'
        return response


class PrintableReportView(View):
    def get(self, request, pk):
        prediction = get_object_or_404(
            Prediction.objects.select_related('uploaded_image', 'user', 'diagnosis', 'fruit_ref', 'disease_ref'),
            pk=pk
        )
        # Allow anonymous predictions or the authenticated owner/admin
        is_owner = (prediction.user is None) or (request.user.is_authenticated and prediction.user == request.user)
        is_admin = request.user.is_authenticated and (
            request.user.is_superuser or
            (hasattr(request.user, 'profile') and request.user.profile.is_admin)
        )
        if not (is_owner or is_admin):
            messages.error(request, "Permission denied.")
            return redirect('home')
        diagnosis = getattr(prediction, 'diagnosis', None)
        return render(request, 'print_report.html', {
            'prediction': prediction,
            'diagnosis': diagnosis
        })

