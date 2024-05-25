# BalduApp/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, SignupForm, MessageForm, NewChatForm
from .models import Chat, Recommendation, User

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
def profile(request):
    return render(request, 'BalduApp/profile.html')

@login_required
def main_page(request):
    chats = Chat.objects.filter(participants=request.user)
    recommendations = Recommendation.objects.filter(user=request.user)

    chat_users = []
    for chat in chats:
        other_user = chat.participants.exclude(id=request.user.id).first()
        chat_users.append({'chat_id': chat.id, 'username': other_user.username if other_user else "Unknown"})

    if request.method == 'POST':
        form = NewChatForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            user = get_object_or_404(User, username=username)
            chat = Chat.objects.filter(participants=request.user).filter(participants=user).first()
            if not chat:
                chat = Chat.objects.create()
                chat.participants.add(request.user, user)
            return redirect('chat_detail', chat_id=chat.id)
    else:
        form = NewChatForm()

    return render(request, 'BalduApp/main_page.html', {
        'chat_users': chat_users,
        'recommendations': recommendations,
        'form': form
    })


@login_required
def new_chat(request):
    if request.method == 'POST':
        form = NewChatForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            user = get_object_or_404(User, username=username)
            chat, created = Chat.objects.get_or_create(participants__in=[request.user, user])
            chat.participants.add(request.user, user)
            return redirect('chat_detail', chat_id=chat.id)
    else:
        form = NewChatForm()
    return render(request, 'BalduApp/new_chat.html', {'form': form})


@login_required
def chat_detail(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id, participants=request.user)
    other_user = chat.participants.exclude(id=request.user.id).first()

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.chat = chat
            message.sender = request.user
            message.save()
            return redirect('chat_detail', chat_id=chat.id)
    else:
        form = MessageForm()

    messages = chat.messages.all()
    return render(request, 'BalduApp/chat_detail.html', {
        'chat': chat,
        'other_user': other_user,
        'messages': messages,
        'form': form
    })
