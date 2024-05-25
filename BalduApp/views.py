# BalduApp/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, SignupForm
from .models import Chat, Recommendation

def startPage(request): # Сторінка з вибором реєстрації або логіном
    return render(request, 'BalduApp/startPage.html')

def register(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'BalduApp/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('profile')
    else:
        form = LoginForm()
    return render(request, 'BalduApp/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def main_page(request):
    chats = Chat.objects.filter(participants=request.user)
    recommendations = Recommendation.objects.filter(user=request.user)

    chat_users = []
    for chat in chats:
        other_user = chat.participants.exclude(id=request.user.id).first()
        chat_users.append(other_user.username if other_user else "Unknown")

    return render(request, 'BalduApp/main_page.html', {
        'chat_users': chat_users,
        'recommendations': recommendations
    })

@login_required
def profile(request):
    return render(request, 'BalduApp/profile.html')

