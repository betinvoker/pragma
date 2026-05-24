from django.db import models

# ==========================================
# Чат AI-консультанта (CONSULTATION)
# ==========================================
class Consultation(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='consultations', verbose_name='Пользователь')
    question = models.TextField('Текст вопроса', max_length=5096)
    answer = models.TextField('Текст ответа', max_length=10192)
    datetime_create = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        db_table = 'consultation'
        verbose_name = 'Консультация'
        verbose_name_plural = 'Консультации'

    def __str__(self):
        return f"Вопрос от {self.user} от {self.datetime_create.strftime('%Y-%m-%d %H:%M')}"