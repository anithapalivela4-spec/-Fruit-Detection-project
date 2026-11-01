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
            full_name = form.cleaned_data['full_name'].strip()
            email = form.cleaned_data['email'].strip().lower()
            password = form.cleaned_data['password']

            # Check duplicate email
            if User.objects.filter(email__iexact=email).exists():
                messages.error(request, "An account with this email address already exists. Please login instead.")
                return render(request, 'register.html', {'form': form})

            # Split full name into first and last name
            name_parts = full_name.split(' ', 1)
            first_name = name_parts[0]
            last_name = name_parts[1] if len(name_parts) > 1 else ''

            # Generate unique username from email
            base_username = email.split('@')[0]
            username = base_username
            counter = 1
            while User.objects.filter(username__iexact=username).exists():
                username = f"{base_username}{counter}"
                counter += 1

            # Securely store user with hashed password
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )

            # Ensure associated UserProfile exists
            profile, _ = UserProfile.objects.get_or_create(user=user)
            profile.role = 'farmer'
            profile.save()

            messages.success(request, f"Registration successful for {full_name}! Please login with your email and password.")
            # Automatically redirect user to LOGIN PAGE (do not open dashboard directly)
            return redirect('accounts:login')
        else:
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
            login_id = form.cleaned_data['email'].strip()
            password = form.cleaned_data['password']

            # Verify credentials from database (supports registered email or username)
            user = None
            try:
                user_obj = User.objects.filter(email__iexact=login_id).first()
                if user_obj:
                    user = authenticate(request, username=user_obj.username, password=password)
            except Exception:
                user = None

            if user is None:
                user = authenticate(request, username=login_id, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {user.get_full_name() or user.username}!")
                next_url = request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                # Redirect user to DASHBOARD
                return redirect('dashboard')
            else:
                messages.error(request, "Invalid email or password. Please verify your credentials and try again.")
        else:
            messages.error(request, "Please enter both email and password.")
        return render(request, 'login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out successfully. Please log in to continue.")
    return redirect('accounts:login')


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
