# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm, ProfileUpdateForm
from news.models import News
from .models import Profile

# Custom login view
def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome, {username}!")
                return redirect('/')  # Redirect to your desired page
            else:
                messages.error(request, "Invalid username or password")
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})

# Custom logout view
def custom_logout(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('/')  # Redirect to login after logout

# Custom register view# accounts/views.py
def custom_register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"Account created for {username}!")

            # Automatically log in the user after registration
            login(request, user)
            
            return redirect('/')  # Redirect to the home page after login
    else:
        form = UserCreationForm()

    return render(request, 'accounts/register.html', {'form': form})






@login_required
def profile(request):
    # Check if the user has a profile, if not, create one
    try:
        request.user.profile
    except Profile.DoesNotExist:
        Profile.objects.create(user=request.user)

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('accounts:profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    # Fetch user's news posts
    user_news = News.objects.filter(user=request.user)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'user_news': user_news,
    }
    return render(request, 'accounts/profile.html', context)




