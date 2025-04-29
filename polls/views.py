from django.shortcuts import render

# Create your views here.
# core/views.py
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Survey

@login_required
def home(request):
    surveys = Survey.objects.filter(is_active=True)
    return render(request, 'registration/home.html', {'surveys': surveys})


def survey_detail(request, survey_id):
    survey = get_object_or_404(Survey, id=survey_id)
    questions = survey.questions.all()

    questions_with_choices = []
    for question in questions:
        choices = question.choices.all()  # <- если related_name='Choices'
        questions_with_choices.append({'question': question, 'choices': choices})

    return render(request, 'registration/survey_detail.html', {
        'survey': survey,
        'questions_with_choices': questions_with_choices
    })

