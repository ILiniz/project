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
    # Удаляем старые ответы пользователя на этот опрос
    Answer.objects.filter(user=request.user, survey=survey).delete()

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
                    choice=choice
                )
            except Choice.DoesNotExist:
                continue  # Если вариант не найден, просто пропускаем

    # Обновляем или создаём отзыв
    feedback_text = request.POST.get('feedback')
    if feedback_text:
        Feedback.objects.update_or_create(
            user=request.user,
            survey=survey,
            defaults={'text': feedback_text}
        )


# Получение всех ответов и отзыва пользователя для опроса
def get_user_answers_and_feedback(user, survey):
    answers = Answer.objects.filter(user=user, survey=survey)
    feedback = Feedback.objects.filter(user=user, survey=survey).first()
    return answers, feedback