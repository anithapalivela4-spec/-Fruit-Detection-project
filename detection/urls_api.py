from django.urls import path
from .api_views import (
    FruitListAPIView,
    DiseaseListAPIView,
    PredictAPIView,
    HistoryAPIView,
    OntologyQueryAPIView
)

urlpatterns = [
    path('fruits/', FruitListAPIView.as_view(), name='api_fruits'),
    path('diseases/', DiseaseListAPIView.as_view(), name='api_diseases'),
    path('predict/', PredictAPIView.as_view(), name='api_predict'),
    path('history/', HistoryAPIView.as_view(), name='api_history'),
    path('ontology/', OntologyQueryAPIView.as_view(), name='api_ontology'),
]
