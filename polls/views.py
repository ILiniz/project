from django.shortcuts import render

# Create your views here.
# core/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Survey, Answer, Feedback
from .logic import (
    process_survey_submission,
    get_survey_questions_with_choices,
    get_user_answers_and_feedback
)
from django.http import JsonResponse
from django.urls import reverse


@login_required
def home(request):
    surveys = Survey.objects.filter(is_active=True)
    return render(request, 'registration/home.html', {'surveys': surveys})


@login_required
def survey_detail(request, survey_id):
    survey = get_object_or_404(Survey, id=survey_id)

    if request.method == 'POST':
        process_survey_submission(request, survey)
        request.session['last_survey_id'] = survey.id

        # ➤ Отвечаем по-разному в зависимости от типа запроса
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'redirect_url': reverse('thanks', args=[survey.id])})
        return redirect('thanks', survey_id=survey.id)

    questions_with_choices = get_survey_questions_with_choices(survey)
    return render(request, 'registration/survey_detail.html', {
        'survey': survey,
        'questions_with_choices': questions_with_choices
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
    return render(request, 'registration/profile.html', {'user': request.user})