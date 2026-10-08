from django.urls import path
from .views import RegisterView, LoginView, logout_view, profile_view, user_list_view

app_name = 'accounts'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name='profile'),
    path('users/', user_list_view, name='users_list'),
]
