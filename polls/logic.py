from .models import Survey, Answer, Feedback, Choice

# Получение всех активных опросов
def get_active_surveys():
    return Survey.objects.filter(is_active=True)


# Получение всех вопросов с вариантами ответов для конкретного опроса
def get_survey_questions_with_choices(survey):
    questions_with_choices = []
    for question in survey.questions.all():
        choices = question.choices.all()
        questions_with_choices.append({'question': question, 'choices': choices})
    return questions_with_choices


# Обработка отправки формы с опросом (ответы + отзыв)
def process_survey_submission(request, survey):
    from .forms import SurveyForm  # импортируем, если ещё не был

    form = SurveyForm(survey, request.POST)
    if not form.is_valid():
        print("❌ Форма невалидна!")
        print(form.errors)
        request.session['form_errors'] = form.errors.as_json()
        return  # можно добавить обработку ошибок при желании

    # Получаем флаг анонимности
    is_anonymous = form.cleaned_data.get('anonymous', False)

    # Удаляем старые ответы пользователя на этот опрос
    Answer.objects.filter(user=request.user, survey=survey).delete()
    Feedback.objects.filter(user=request.user, survey=survey).delete()

    # Сохраняем новые ответы
    for question in survey.questions.all():
        choice_id = request.POST.get(f'question_{question.id}')
        if choice_id:
            try:
                choice = Choice.objects.get(id=choice_id)
                Answer.objects.create(
                    user=request.user,
                    survey=survey,
                    question=question,
                    choice=choice,
                    is_anonymous=is_anonymous
                )
            except Choice.DoesNotExist:
                continue

    # Сохраняем отзыв
    feedback_text = form.cleaned_data.get('feedback')
    if feedback_text:
        Feedback.objects.create(
            user=request.user,
            survey=survey,
            text=feedback_text,
            is_anonymous=is_anonymous
        )


# Получение всех ответов и отзыва пользователя для опроса
def get_user_answers_and_feedback(user, survey):
    answers = Answer.objects.filter(user=user, survey=survey)
    feedback = Feedback.objects.filter(user=user, survey=survey).first()
    return answers, feedback