# polls/urls.py
from django.urls import path
from . import views  # импортируем представления из нашего приложения

urlpatterns = [
    path('home/', views.employee_home, name='employee_home'),  # путь для домашней страницы
    path('survey/<int:survey_id>/', views.survey_detail, name='survey_detail'),
    path('thanks/<int:survey_id>/', views.thanks, name='thanks'),
    path('profile/', views.profile, name='profile'),
    path('completed/', views.completed_surveys, name='completed'),
    path('completed/<int:survey_id>/answers/', views.view_user_answers, name='view_user_answers'),
    path('survey/<int:survey_id>/reset/', views.reset_survey_progress, name='reset_survey_progress'),
    path('manager/home/', views.manager_home, name='manager_home'),
    path('manager/employee/<int:user_id>/', views.employee_detail, name='employee_detail'),
]

