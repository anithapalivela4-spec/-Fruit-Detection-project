from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Disease, Symptom, Treatment, Prevention, EnvironmentalFactor
from fruits.models import Fruit
from .forms import DiseaseForm, SymptomForm, TreatmentForm, PreventionForm

def disease_list_view(request):
    fruit_id = request.GET.get('fruit')
    severity = request.GET.get('severity')
    query = request.GET.get('q', '').strip()

    diseases = Disease.objects.all().select_related('affected_fruit')
    if fruit_id:
        diseases = diseases.filter(affected_fruit_id=fruit_id)
    if severity:
        diseases = diseases.filter(severity=severity)
    if query:
        diseases = diseases.filter(disease_name__icontains=query) | diseases.filter(description__icontains=query)

    fruits = Fruit.objects.all()
    return render(request, 'diseases.html', {
        'diseases': diseases,
        'fruits': fruits,
        'selected_fruit': int(fruit_id) if fruit_id and fruit_id.isdigit() else None,
        'selected_severity': severity,
        'query': query,
    })

def disease_detail_view(request, pk):
    disease = get_object_or_404(
        Disease.objects.select_related('affected_fruit').prefetch_related(
            'symptoms', 'environmental_factors', 'treatments', 'preventions'
        ),
        pk=pk
    )
    return render(request, 'disease_detail.html', {'disease': disease})

@login_required
def disease_create_view(request):
    if not (request.user.is_superuser or request.user.profile.is_expert):
        messages.error(request, "Permission denied. Only agricultural experts or admins can add diseases.")
        return redirect('diseases:disease_list')
    if request.method == 'POST':
        form = DiseaseForm(request.POST, request.FILES)
        if form.is_valid():
            disease = form.save()
            messages.success(request, f"Disease '{disease.disease_name}' added successfully.")
            return redirect('diseases:disease_detail', pk=disease.pk)
    else:
        form = DiseaseForm()
    return render(request, 'disease_form.html', {'form': form, 'title': 'Add New Disease'})

@login_required
def disease_update_view(request, pk):
    disease = get_object_or_404(Disease, pk=pk)
    if not (request.user.is_superuser or request.user.profile.is_expert):
        messages.error(request, "Permission denied.")
        return redirect('diseases:disease_detail', pk=disease.pk)
    if request.method == 'POST':
        form = DiseaseForm(request.POST, request.FILES, instance=disease)
        if form.is_valid():
            form.save()
            messages.success(request, f"Disease '{disease.disease_name}' updated successfully.")
            return redirect('diseases:disease_detail', pk=disease.pk)
    else:
        form = DiseaseForm(instance=disease)
    return render(request, 'disease_form.html', {'form': form, 'disease': disease, 'title': f'Edit {disease.disease_name}'})

@login_required
def disease_delete_view(request, pk):
    disease = get_object_or_404(Disease, pk=pk)
    if not (request.user.is_superuser or request.user.profile.is_admin):
        messages.error(request, "Permission denied. Only admins can delete records.")
        return redirect('diseases:disease_detail', pk=disease.pk)
    if request.method == 'POST':
        name = disease.disease_name
        disease.delete()
        messages.success(request, f"Disease '{name}' removed successfully.")
        return redirect('diseases:disease_list')
    return render(request, 'confirm_delete.html', {'object': disease, 'type': 'Disease', 'cancel_url': disease.get_absolute_url()})

# Symptom management
@login_required
def symptom_list_view(request):
    symptoms = Symptom.objects.all().prefetch_related('diseases')
    form = SymptomForm()
    if request.method == 'POST' and (request.user.is_superuser or request.user.profile.is_expert):
        form = SymptomForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Symptom added successfully.")
            return redirect('diseases:symptom_list')
    return render(request, 'symptoms_list.html', {'symptoms': symptoms, 'form': form})

# Treatment management
@login_required
def treatment_list_view(request):
    treatments = Treatment.objects.all().prefetch_related('diseases')
    form = TreatmentForm()
    if request.method == 'POST' and (request.user.is_superuser or request.user.profile.is_expert):
        form = TreatmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Treatment added successfully.")
            return redirect('diseases:treatment_list')
    return render(request, 'treatments_list.html', {'treatments': treatments, 'form': form})

# Prevention management
@login_required
def prevention_list_view(request):
    preventions = Prevention.objects.all().prefetch_related('diseases')
    form = PreventionForm()
    if request.method == 'POST' and (request.user.is_superuser or request.user.profile.is_expert):
        form = PreventionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Prevention guideline added successfully.")
            return redirect('diseases:prevention_list')
    return render(request, 'preventions_list.html', {'preventions': preventions, 'form': form})
