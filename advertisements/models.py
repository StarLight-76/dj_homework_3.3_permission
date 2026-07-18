from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Advertisement(models.Model):
    """
    Модель объявления.
    """
    OPEN = 'OPEN'
    CLOSED = 'CLOSED'
    DRAFT = 'DRAFT'
    STATUS_CHOICES = [
        (OPEN, 'Открыто'),
        (CLOSED, 'Закрыто'),
        (DRAFT, 'Черновик'),
    ]

    title = models.CharField(max_length=200, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=DRAFT, verbose_name='Статус')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='advertisements', verbose_name='Автор')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'
        ordering = ['-created_at']

    def __str__(self):
        return self.title