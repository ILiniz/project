# polls/urls.py
from django.urls import path
from . import views  # импортируем представления из нашего приложения

urlpatterns = [
    path('home/', views.home, name='home'),  # путь для домашней страницы
    path('survey/<int:survey_id>/', views.survey_detail, name='survey_detail'),
    path('thanks/<int:survey_id>/', views.thanks, name='thanks'),
    path('profile/', views.profile, name='profile'),
]

