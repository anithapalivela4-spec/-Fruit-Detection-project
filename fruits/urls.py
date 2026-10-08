from django.urls import path
from .views import fruit_list_view, fruit_detail_view, fruit_create_view, fruit_update_view, fruit_delete_view

app_name = 'fruits'

urlpatterns = [
    path('', fruit_list_view, name='fruit_list'),
    path('add/', fruit_create_view, name='fruit_create'),
    path('<int:pk>/', fruit_detail_view, name='fruit_detail'),
    path('<int:pk>/edit/', fruit_update_view, name='fruit_update'),
    path('<int:pk>/delete/', fruit_delete_view, name='fruit_delete'),
]
