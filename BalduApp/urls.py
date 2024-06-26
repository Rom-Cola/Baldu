from django.conf.urls.static import static
from django.urls import path

from Baldu import settings
from BalduApp.views import register, login_view, logout_view, profile, startPage, main_page, chat_detail

urlpatterns = [
    path('', startPage, name='startPage'), # початкова сторінка з вибором реєстрації або логіном
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile, name='profile'),
    path('main/', main_page, name='main_page'),
    path('chat/<int:chat_id>/', chat_detail, name='chat_detail'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


