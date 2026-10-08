from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.views import View
from django.utils.decorators import method_decorator

from .forms import UserRegistrationForm, UserLoginForm, UserProfileUpdateForm
from .models import UserProfile


class RegisterView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('dashboard')
        form = UserRegistrationForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            role = form.cleaned_data['role']
            phone = form.cleaned_data.get('phone', '')
            farm_location = form.cleaned_data.get('farm_location', '')

            if User.objects.filter(username=username).exists():
                messages.error(request, "Username is already taken. Please choose another.")
                return render(request, 'register.html', {'form': form})

            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            # Update created profile
            profile = user.profile
            profile.role = role
            profile.phone = phone
            profile.farm_location = farm_location
            profile.save()

            messages.success(request, f"Welcome {username}! Your account has been registered successfully. Please log in.")
            return redirect('accounts:login')
        return render(request, 'register.html', {'form': form})


class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('dashboard')
        form = UserLoginForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = UserLoginForm(request.POST)
        if form.is_valid():
            login_id = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Allow login with either username or email
            user = authenticate(request, username=login_id, password=password)
            if user is None:
                try:
                    user_obj = User.objects.get(email=login_id)
                    user = authenticate(request, username=user_obj.username, password=password)
                except User.DoesNotExist:
                    user = None

            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {user.get_full_name() or user.username}!")
                next_url = request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                if user.is_superuser or (hasattr(user, 'profile') and user.profile.is_admin):
                    return redirect('detection:admin_dashboard')
                return redirect('dashboard')
            else:
                messages.error(request, "Invalid username/email or password.")
        return render(request, 'login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect('home')


@login_required
def profile_view(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = UserProfileUpdateForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            request.user.first_name = form.cleaned_data['first_name']
            request.user.last_name = form.cleaned_data['last_name']
            request.user.email = form.cleaned_data['email']
            request.user.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('accounts:profile')
    else:
        form = UserProfileUpdateForm(instance=profile)

    return render(request, 'profile.html', {'form': form, 'profile': profile})


@login_required
def user_list_view(request):
    if not (request.user.is_superuser or request.user.profile.is_admin):
        messages.error(request, "Access restricted to administrators.")
        return redirect('dashboard')
    users = User.objects.all().select_related('profile').order_by('-date_joined')
    return render(request, 'users_list.html', {'users': users})
