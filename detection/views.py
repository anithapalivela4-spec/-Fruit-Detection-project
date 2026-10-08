import os
import json
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


@method_decorator(login_required, name='dispatch')
class DashboardView(View):
    def get(self, request):
        user = request.user
        predictions = Prediction.objects.filter(user=user).select_related('diagnosis', 'uploaded_image')

        total_predictions = predictions.count()
        healthy_results = predictions.filter(disease_name__icontains='healthy').count()
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


@method_decorator(login_required, name='dispatch')
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

            # 1. Save uploaded image
            uploaded_img_obj = UploadedImage.objects.create(
                user=request.user,
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
                user=request.user,
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

            messages.success(request, f"Image processed successfully: {prediction_record.disease_name} detected.")
            return redirect('detection:result', pk=prediction_record.pk)

        fruits = Fruit.objects.all()
        return render(request, 'upload.html', {'form': form, 'fruits': fruits})


@method_decorator(login_required, name='dispatch')
class ResultView(View):
    def get(self, request, pk):
        prediction = get_object_or_404(
            Prediction.objects.select_related('uploaded_image', 'user', 'diagnosis', 'fruit_ref', 'disease_ref'),
            pk=pk
        )
        # Check permissions: users can only view their own predictions unless admin
        if not (request.user.is_superuser or request.user.profile.is_admin or prediction.user == request.user):
            messages.error(request, "Permission denied.")
            return redirect('dashboard')

        return render(request, 'result.html', {'prediction': prediction, 'diagnosis': prediction.diagnosis})


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


@method_decorator(login_required, name='dispatch')
class ExportReportView(View):
    def get(self, request, pk):
        prediction = get_object_or_404(
            Prediction.objects.select_related('uploaded_image', 'user', 'diagnosis'),
            pk=pk
        )
        if not (request.user.is_superuser or request.user.profile.is_admin or prediction.user == request.user):
            messages.error(request, "Permission denied.")
            return redirect('dashboard')

        report_content = generate_text_report(prediction)
        response = HttpResponse(report_content, content_type='text/plain; charset=utf-8')
        response['Content-Disposition'] = f'attachment; filename="FruitDisease_Report_{prediction.id}.txt"'
        return response
