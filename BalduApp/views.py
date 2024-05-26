# BalduApp/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, SignupForm, MessageForm, NewChatForm, LikeForm, DislikeForm, UserEditForm
from .models import Chat, Recommendation, User, Dislike, Message


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
    error_message = None  # Додаємо змінну для збереження повідомлення про помилку
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
                error_message = "Неправильний логін або пароль"  # Повідомлення про помилку
                return render(request, 'BalduApp/login.html', {'form': form, 'error': error_message})
    else:
        form = LoginForm()

    return render(request, 'BalduApp/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')



@login_required
def profile(request):
    if request.method == 'POST':
        form = UserEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserEditForm(instance=request.user)
    return render(request, 'BalduApp/profile.html', {'form': form})

@login_required
def main_page(request):
    chats = Chat.objects.filter(participants=request.user)
    recommendations = Recommendation.objects.filter(user=request.user)
    dislikes = Dislike.objects.filter(user=request.user)

    chat_users = []
    for chat in chats:
        other_user = chat.participants.exclude(id=request.user.id).first()
        chat_users.append({'chat_id': chat.id, 'username': other_user.username if other_user else "Unknown"})

    recommended_users = User.objects.exclude(id=request.user.id).exclude(recommended_to__user=request.user).exclude(disliked_by__user=request.user)

    if 'recommended_index' not in request.session:
        request.session['recommended_index'] = 0

    recommended_users = list(recommended_users)
    if recommended_users:
        current_recommended_user = recommended_users[request.session['recommended_index'] % len(recommended_users)]
    else:
        current_recommended_user = None

    if request.method == 'POST':
        if 'like' in request.POST:
            like_form = LikeForm(request.POST)
            if like_form.is_valid():
                user_id = like_form.cleaned_data['user_id']
                user = get_object_or_404(User, id=user_id)
                chat = Chat.objects.filter(participants=request.user).filter(participants=user).first()
                if not chat:
                    chat = Chat.objects.create()
                    chat.participants.add(request.user, user)
                Message.objects.create(chat=chat, sender=request.user, content="Hi! Let's chat!")
                Recommendation.objects.create(user=request.user, recommended_user=user)
                request.session['recommended_index'] += 1
                return redirect('main_page')
        elif 'dislike' in request.POST:
            dislike_form = DislikeForm(request.POST)
            if dislike_form.is_valid():
                user_id = dislike_form.cleaned_data['user_id']
                user = get_object_or_404(User, id=user_id)
                Dislike.objects.create(user=request.user, disliked_user=user)
                request.session['recommended_index'] += 1
                return redirect('main_page')
        elif 'start_chat' in request.POST:
            form = NewChatForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                try:
                    user = User.objects.get(username=username)
                    chat = Chat.objects.filter(participants=request.user).filter(participants=user).first()
                    if not chat:
                        chat = Chat.objects.create()
                        chat.participants.add(request.user, user)
                    return redirect('chat_detail', chat_id=chat.id)
                except User.DoesNotExist:
                    error_message = "Таку людину не було знайдено"
                    return render(request, 'BalduApp/main_page.html', {
                        'chat_users': chat_users,
                        'recommendations': recommendations,
                        'current_recommended_user': current_recommended_user,
                        'form': form,
                        'like_form': LikeForm,
                        'dislike_form': Dislike,
                        'error_message': error_message
                    })
    else:
        form = NewChatForm()
        like_form = LikeForm()
        dislike_form = DislikeForm()

    return render(request, 'BalduApp/main_page.html', {
        'chat_users': chat_users,
        'recommendations': recommendations,
        'current_recommended_user': current_recommended_user,
        'form': form,
        'like_form': like_form,
        'dislike_form': dislike_form
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