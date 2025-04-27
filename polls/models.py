from django.db import models

# Create your models here.
from django.db import models

class Survey(models.Model):
    name = models.CharField(max_length=100)  # Название опроса
    description = models.TextField()  # Описание опроса
    is_active = models.BooleanField(default=True)  # Статус (активен ли опрос)

    def __str__(self):
        return self.name

class Question(models.Model):
    survey = models.ForeignKey(Survey, related_name='questions', on_delete=models.CASCADE, default=1)
    text = models.CharField(max_length=255, default='text')

    def __str__(self):
        return self.text

class Choice(models.Model):
    question = models.ForeignKey(Question, related_name='Choices', on_delete=models.CASCADE, default=1)
    text = models.CharField(max_length=255, default='text')

    def __str__(self):
        return self.text

