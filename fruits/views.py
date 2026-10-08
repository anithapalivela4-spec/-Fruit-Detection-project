from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Fruit
from .forms import FruitForm

def fruit_list_view(request):
    query = request.GET.get('q', '').strip()
    if query:
        fruits = Fruit.objects.filter(fruit_name__icontains=query) | Fruit.objects.filter(description__icontains=query)
    else:
        fruits = Fruit.objects.all()
    return render(request, 'fruits.html', {'fruits': fruits, 'query': query})

def fruit_detail_view(request, pk):
    fruit = get_object_or_404(Fruit, pk=pk)
    diseases = fruit.diseases.all().prefetch_related('symptoms', 'treatments', 'preventions')
    return render(request, 'fruit_detail.html', {'fruit': fruit, 'diseases': diseases})

@login_required
def fruit_create_view(request):
    if not (request.user.is_superuser or request.user.profile.is_expert):
        messages.error(request, "Permission denied. Only agricultural experts or admins can add fruits.")
        return redirect('fruits:fruit_list')
    if request.method == 'POST':
        form = FruitForm(request.POST, request.FILES)
        if form.is_valid():
            fruit = form.save()
            messages.success(request, f"Fruit '{fruit.fruit_name}' added successfully.")
            return redirect('fruits:fruit_detail', pk=fruit.pk)
    else:
        form = FruitForm()
    return render(request, 'fruit_form.html', {'form': form, 'title': 'Add New Fruit'})

@login_required
def fruit_update_view(request, pk):
    fruit = get_object_or_404(Fruit, pk=pk)
    if not (request.user.is_superuser or request.user.profile.is_expert):
        messages.error(request, "Permission denied.")
        return redirect('fruits:fruit_detail', pk=fruit.pk)
    if request.method == 'POST':
        form = FruitForm(request.POST, request.FILES, instance=fruit)
        if form.is_valid():
            form.save()
            messages.success(request, f"Fruit '{fruit.fruit_name}' updated successfully.")
            return redirect('fruits:fruit_detail', pk=fruit.pk)
    else:
        form = FruitForm(instance=fruit)
    return render(request, 'fruit_form.html', {'form': form, 'fruit': fruit, 'title': f'Edit {fruit.fruit_name}'})

@login_required
def fruit_delete_view(request, pk):
    fruit = get_object_or_404(Fruit, pk=pk)
    if not (request.user.is_superuser or request.user.profile.is_admin):
        messages.error(request, "Permission denied. Only admins can delete records.")
        return redirect('fruits:fruit_detail', pk=fruit.pk)
    if request.method == 'POST':
        name = fruit.fruit_name
        fruit.delete()
        messages.success(request, f"Fruit '{name}' removed successfully.")
        return redirect('fruits:fruit_list')
    return render(request, 'confirm_delete.html', {'object': fruit, 'type': 'Fruit', 'cancel_url': fruit.get_absolute_url()})
