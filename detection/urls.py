from django.urls import path
from .views import (
    UploadAndDetectView,
    ResultView,
    HistoryView,
    DeletePredictionView,
    ExportReportView,
    PrintableReportView,
    AdminDashboardView
)

app_name = 'detection'

urlpatterns = [
    path('detect/', UploadAndDetectView.as_view(), name='detect'),
    path('result/<int:pk>/', ResultView.as_view(), name='result'),
    path('history/', HistoryView.as_view(), name='history'),
    path('delete/<int:pk>/', DeletePredictionView.as_view(), name='delete_prediction'),
    path('report/<int:pk>/', ExportReportView.as_view(), name='export_report'),
    path('report/print/<int:pk>/', PrintableReportView.as_view(), name='print_report'),
    path('admin-dashboard/', AdminDashboardView.as_view(), name='admin_dashboard'),
]
