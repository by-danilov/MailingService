from django.db import models
from django.conf import settings
from datetime import time, date

class Client(models.Model):
    """Модель получателя рассылки (Клиент)."""
    email = models.EmailField(unique=True, verbose_name="Email")
    full_name = models.CharField(max_length=150, verbose_name="ФИО")
    comment = models.TextField(blank=True, null=True, verbose_name="Комментарий")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"
        permissions = [
            ("can_deactivate_client", "Can deactivate clients"),
        ]

class Message(models.Model):
    """Модель содержимого письма (Сообщение)."""
    subject = models.CharField(max_length=200, verbose_name="Тема письма")
    body = models.TextField(verbose_name="Тело письма")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        permissions = [
            ("can_view_all_messages", "Can view all messages"),
        ]

class Mailing(models.Model):
    """Модель рассылки с настройками планирования."""
    FREQUENCY_CHOICES = [
        ('daily', 'Ежедневно'),
        ('weekly', 'Еженедельно'),
        ('monthly', 'Ежемесячно'),
    ]
    STATUS_CHOICES = [
        ('created', 'Создана'),
        ('started', 'Запущена'),
        ('completed', 'Завершена'),
    ]

    start_date = models.DateField(default=date.today, verbose_name="Дата начала")
    start_time = models.TimeField(default=time(8, 0), verbose_name="Время начала")
    end_date = models.DateField(verbose_name="Дата окончания")
    frequency = models.CharField(max_length=10, choices=FREQUENCY_CHOICES, verbose_name="Периодичность")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='created', verbose_name="Статус")
    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name="Сообщение")
    clients = models.ManyToManyField(Client, verbose_name="Клиенты")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"Рассылка от {self.start_date}"

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        permissions = [
            ("can_deactivate_mailing", "Can deactivate mailings"),
            ("can_view_all_attempts", "Can view all mailing attempts"),
        ]

class MailingAttempt(models.Model):
    """Модель попытки отправки рассылки (Лог)."""
    STATUS_CHOICES = [
        ('success', 'Успешно'),
        ('failed', 'Неуспешно'),
    ]
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name="Рассылка")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Дата и время попытки")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, verbose_name="Статус")
    server_response = models.TextField(blank=True, null=True, verbose_name="Ответ сервера")

    def __str__(self):
        return f"Попытка для {self.mailing} в {self.timestamp}"

    class Meta:
        verbose_name = "Попытка рассылки"
        verbose_name_plural = "Попытки рассылок"
