from django.db import models


class Question(models.Model):
    """
    Модель для вопроса.
    """
    text = models.TextField(verbose_name="Текст вопроса")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")

    def __str__(self):
        return f"Вопрос №{self.id}"

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"
        ordering = ['-created_at']


class Answer(models.Model):
    """
    Модель для ответа на вопрос.
    """
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='answers',
        verbose_name="Вопрос"
    )
    user_id = models.CharField(max_length=255, verbose_name="ID пользователя")
    text = models.TextField(verbose_name="Текст ответа")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")

    def __str__(self):
        return f"Ответ №{self.id} на вопрос №{self.question.id}"

    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"
        ordering = ['created_at']
