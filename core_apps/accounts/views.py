# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib import messages
import json

from .forms import CustomUserCreationForm, CustomAuthenticationForm
from .models import UserProfile

class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'accounts/login.html'
    success_url = reverse_lazy('posts:home')

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('posts:home')

@require_http_methods(["POST"])
def ajax_register(request):
    try:
        data = json.loads(request.body)
        form = CustomUserCreationForm(data)
        
        if form.is_valid():
            user = form.save()
            # Create user profile
            UserProfile.objects.create(user=user)
            
            # Authenticate and login
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            
            if user:
                login(request, user)
                return JsonResponse({
                    'success': True,
                    'message': 'Registration successful!',
                    'redirect_url': '/'
                })
        else:
            return JsonResponse({
                'success': False,
                'errors': form.errors
            })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': 'An error occurred during registration.'
        })

@require_http_methods(["POST"])
def ajax_login(request):
    try:
        data = json.loads(request.body)
        form = CustomAuthenticationForm(data=data)
        print("..................")
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user:
                login(request, user)
                return JsonResponse({
                    'success': True,
                    'message': 'Login successful!',
                    'redirect_url': '/'
                })
        else:
            return JsonResponse({
                'success': False,
                'errors': form.errors
            })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': 'An error occurred during login.'
        })

def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    form = CustomUserCreationForm()
    return render(request, 'user/auth/signup.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    form = CustomAuthenticationForm()
    return render(request, 'user/auth/signin.html', {'form': form})

@login_required
def profile_view(request, username=None):
    if username:
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return redirect('home')
    else:
        user = request.user
    
    profile, created = UserProfile.objects.get_or_create(user=user)
    posts = user.post_set.all().order_by('-created_at')
    comments = user.comment_set.all().order_by('-created_at')
    
    context = {
        'profile_user': user,
        'profile': profile,
        'posts': posts,
        'comments': comments,
    }
    return render(request, 'user/profile/profile.html', context)

    
@login_required
def ajax_edit_profile(request):
    if request.method == 'POST':
        user = request.user
        profile, _ = UserProfile.objects.get_or_create(user=user)

        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        profile.bio = request.POST.get('bio', profile.bio)

        if request.FILES.get('avatar'):
            profile.avatar = request.FILES['avatar']

        user.save()
        profile.save()

        return JsonResponse({'success': True, 'message': 'Profile updated successfully'})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)