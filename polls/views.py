from django.shortcuts import render

# Create your views here.
# core/views.py
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Survey
from .forms import SurveyForm

@login_required
def home(request):
    surveys = Survey.objects.filter(is_active=True)
    return render(request, 'registration/home.html', {'surveys': surveys})

def survey_detail(request, survey_id):
    survey = get_object_or_404(Survey, id=survey_id)
    return render(request, 'registration/survey_detail.html', {'survey': survey})

def survey_view(request, survey_id):
    survey = Survey.objects.get(id=survey_id)
    if request.method == 'POST':
        form = SurveyForm(survey, request.POST)
        if form.is_valid():
            # Здесь можно обработать ответы, сохранить их или отправить
            # Например, сохранить ответы
            return render(request, 'polls/survey_complete.html')  # Страница с подтверждением
    else:
        form = SurveyForm(survey)
    return render(request, 'polls/survey_detail.html', {'form': form, 'survey': survey})