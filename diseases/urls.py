from django.urls import path
from .views import (
    disease_list_view, disease_detail_view, disease_create_view,
    disease_update_view, disease_delete_view,
    symptom_list_view, treatment_list_view, prevention_list_view
)

app_name = 'diseases'

urlpatterns = [
    path('', disease_list_view, name='disease_list'),
    path('add/', disease_create_view, name='disease_create'),
    path('<int:pk>/', disease_detail_view, name='disease_detail'),
    path('<int:pk>/edit/', disease_update_view, name='disease_update'),
    path('<int:pk>/delete/', disease_delete_view, name='disease_delete'),
    path('symptoms/', symptom_list_view, name='symptom_list'),
    path('treatments/', treatment_list_view, name='treatment_list'),
    path('preventions/', prevention_list_view, name='prevention_list'),
]
