from django import forms

class SurveyForm(forms.Form):
    def __init__(self, survey, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.survey = survey
        for question in survey.questions.all():
            choices = [(choice.id, choice.text) for choice in question.choices.all()]
            self.fields[f'question_{question.id}'] = forms.ChoiceField(
                choices=choices,
                widget=forms.RadioSelect(attrs={'required': False}),
                label=question.text,
                required=True,
                error_messages = {'required': 'Выберите один из вариантов'}
            )
        self.fields['feedback'] = forms.CharField(widget=forms.Textarea, required=False, label='Ваш отзыв')

        if survey.allow_anonymous:
            self.fields['anonymous'] = forms.BooleanField(
                required=False,
                label='Отправить анонимно'
            )