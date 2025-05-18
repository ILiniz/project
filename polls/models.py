# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class Survey(models.Model):
    name = models.CharField(max_length=100)  # Название опроса
    description = models.TextField()  # Описание опроса
    is_active = models.BooleanField(default=True)  # Статус (активен ли опрос)
    allow_anonymous = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Question(models.Model):
    survey = models.ForeignKey(Survey, related_name='questions', on_delete=models.CASCADE, default=1)
    text = models.CharField(max_length=255, default='text')

    def __str__(self):
        return self.text

class Choice(models.Model):
    question = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE, default=1)
    text = models.CharField(max_length=255, default='text')

    def __str__(self):
        return self.text

class Answer(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    survey = models.ForeignKey('Survey', on_delete=models.CASCADE)
    is_anonymous = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.question.text}: {self.choice.text}"


class Feedback(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    text = models.TextField()
    is_anonymous = models.BooleanField(default=False)

    def __str__(self):
        return f"Feedback from {self.user.username} on {self.survey.name}"

    class Meta:
        unique_together = ('user', 'survey')


class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=150)
    position = models.CharField(max_length=100)
    department = models.CharField(max_length=100)

    ROLE_CHOICES = (
        ('user', 'Обычный пользователь'),
        ('manager', 'Руководитель'),
        ('admin', 'Администратор'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')

    def __str__(self):
        return self.username