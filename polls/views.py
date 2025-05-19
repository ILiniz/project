from django.shortcuts import render

# Create your views here.
# core/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Survey, Answer, Feedback, CustomUser
from .logic import (
    process_survey_submission,
    get_survey_questions_with_choices,
    get_user_answers_and_feedback
)
from .forms import SurveyForm
from django.http import JsonResponse
from django.urls import reverse
from django.contrib.auth import logout
from django.contrib import messages
from django.shortcuts import redirect
from django.db.models import Prefetch
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.http import Http404



@login_required
def home(request):
    all_surveys = Survey.objects.filter(is_active=True)
    completed_survey_ids = Answer.objects.filter(user=request.user).values_list('survey_id', flat=True).distinct()
    available_surveys = all_surveys.exclude(id__in=completed_survey_ids)
    return render(request, 'registration/home.html', {'surveys': available_surveys})


@login_required
def survey_detail(request, survey_id):
    survey = get_object_or_404(Survey, id=survey_id)
    questions_with_choices = get_survey_questions_with_choices(survey)

    if request.method == 'POST':

        form = SurveyForm(survey, request.POST)

        if form.is_valid():
            # Обработка + сохранение
            from .logic import process_survey_submission
            process_survey_submission(request, survey)
            return redirect('thanks', survey_id=survey.id)
        else:
            # Форма невалидна → остаёмся на той же странице, с ошибками
            return render(request, 'registration/survey_detail.html', {
                'survey': survey,
                'questions_with_choices': questions_with_choices,
                'form': form,
                'form_errors': form.errors
            })

    questions_with_choices = get_survey_questions_with_choices(survey)
    form = SurveyForm(survey)
    return render(request, 'registration/survey_detail.html', {
        'survey': survey,
        'questions_with_choices': questions_with_choices,
        'form': form
    })


@login_required
def thanks(request, survey_id):
    survey = get_object_or_404(Survey, id=survey_id)
    answers, feedback = get_user_answers_and_feedback(request.user, survey)

    return render(request, 'registration/thanks.html', {
        'survey': survey,
        'answers': answers,
        'feedback': feedback
    })

@login_required
def profile(request):
    if request.user.role == 'manager':
        return render(request, 'manager/profile.html', {'user': request.user})
    else:
        return render(request, 'registration/profile.html', {'user': request.user})

@login_required
def completed_surveys(request):
    user_answers = Answer.objects.filter(user=request.user)
    surveys = Survey.objects.filter(id__in=user_answers.values('survey_id').distinct())
    surveys = surveys.prefetch_related(
        Prefetch('answer_set', queryset=user_answers, to_attr='user_answers')
    )
    return render(request, 'registration/completed.html', {'surveys': surveys})

def custom_logout(request):
    logout(request)
    messages.success(request, "Вы успешно вышли из системы.")
    return redirect('login')

@login_required
def view_user_answers(request, survey_id):
    survey = get_object_or_404(Survey, id=survey_id)
    answers = Answer.objects.filter(user=request.user, survey=survey).select_related('question', 'choice')
    feedback = Feedback.objects.filter(user=request.user, survey=survey).first()

    if not answers.exists():
        return redirect('completed')  # защита: если попытка открыть чужой/непройденный опрос

    return render(request, 'registration/user_answers.html', {
        'survey': survey,
        'answers': answers,
        'feedback': feedback
    })

@login_required
def reset_survey_progress(request, survey_id):
    survey = get_object_or_404(Survey, id=survey_id)
    Answer.objects.filter(user=request.user, survey=survey).delete()
    Feedback.objects.filter(user=request.user, survey=survey).delete()
    messages.success(request, f"Ваши ответы на опрос '{survey.name}' были сброшены.")
    return redirect('employee_home')

@login_required
def role_redirect(request):
    print("ROLE REDIRECT:", request.user.role)
    if request.user.role == 'manager':
        return redirect('manager_home')  # руководитель
    else:
        return redirect('employee_home')  # сотрудник

@login_required
def employee_home(request):
    all_surveys = Survey.objects.filter(is_active=True)
    completed_survey_ids = Answer.objects.filter(user=request.user).values_list('survey_id', flat=True).distinct()
    available_surveys = all_surveys.exclude(id__in=completed_survey_ids)
    return render(request, 'registration/home.html', {'surveys': available_surveys})

@login_required
def manager_home(request):
    employees = CustomUser.objects.filter(
        department=request.user.department,
        role='user'
    )
    return render(request, 'manager/home.html', {
        'user': request.user,
        'employees': employees
    })

class RoleBasedLoginView(LoginView):
    def get_success_url(self):
        return reverse_lazy('role_redirect')

@login_required
def employee_detail(request, user_id):
    User = get_user_model()
    try:
        employee = User.objects.get(id=user_id, role='user')
    except User.DoesNotExist:
        raise Http404("Сотрудник не найден")

    if employee.department != request.user.department:
        raise Http404("Нет доступа к этому сотруднику")

    from .models import Survey, Answer

    # Неанонимные опросы
    answered_survey_ids = Answer.objects.filter(
        user=employee,
        is_anonymous=False  # ← ключевая проверка!
    ).values_list('survey_id', flat=True).distinct()

    answered_surveys = Survey.objects.filter(id__in=answered_survey_ids)

    # Анонимные
    anonymous_survey_ids = Answer.objects.filter(
        user=employee,
        is_anonymous=True
    ).values_list('survey_id', flat=True).distinct()

    anonymous_surveys = Survey.objects.filter(id__in=anonymous_survey_ids)

    return render(request, 'manager/employee_detail.html', {
        'employee': employee,
        'answered_surveys': answered_surveys,
        'anonymous_surveys': anonymous_surveys,
    })

@login_required
def anonymous_surveys_view(request):
    if request.user.role != 'manager':
        raise Http404("Нет доступа")

    # Все опросы, в которых были анонимные ответы
    from .models import Survey, Answer
    anonymous_survey_ids = Answer.objects.filter(
        is_anonymous=True,
        survey__allow_anonymous=True
    ).values_list('survey_id', flat=True).distinct()

    surveys = Survey.objects.filter(id__in=anonymous_survey_ids)

    return render(request, 'manager/anonymous_surveys.html', {
        'surveys': surveys
    })

@login_required
def anonymous_survey_detail(request, survey_id):
    if request.user.role != 'manager':
        raise Http404("Нет доступа")

    from .models import Survey, Answer
    survey = get_object_or_404(Survey, id=survey_id, allow_anonymous=True)

    answers = Answer.objects.filter(
        survey=survey,
        is_anonymous=True
    ).select_related('question', 'choice')

    return render(request, 'manager/anonymous_survey_detail.html', {
        'survey': survey,
        'answers': answers
    })


@login_required
def view_employee_answers(request, user_id, survey_id):
    if request.user.role != 'manager':
        raise Http404("Нет доступа")

    employee = get_object_or_404(CustomUser, id=user_id, role='user')

    # Защита: сотрудник должен быть из отдела руководителя
    if employee.department != request.user.department:
        raise Http404("Нет доступа к сотруднику")

    survey = get_object_or_404(Survey, id=survey_id)
    answers = Answer.objects.filter(user=employee, survey=survey, is_anonymous=False).select_related('question',
                                                                                                     'choice')
    feedback = Feedback.objects.filter(user=employee, survey=survey, is_anonymous=False).first()

    return render(request, 'manager/employee_answers.html', {
        'employee': employee,
        'survey': survey,
        'answers': answers,
        'feedback': feedback,
    })