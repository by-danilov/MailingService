from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """
    Кастомная модель пользователя, наследованная от AbstractUser.
    Использует email в качестве основного поля для авторизации
    и включает дополнительные поля.
    """
    username = None

    email = models.EmailField(
        unique=True,
        verbose_name='Email'
    )

    avatar = models.ImageField(
        upload_to='users/avatars/',
        blank=True,
        null=True,
        verbose_name='Аватар'
    )

    phone = models.CharField(
        max_length=35,
        blank=True,
        null=True,
        verbose_name='Телефон'
    )

    country = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='Страна'
    )

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='users_set',
        related_query_name='user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='users_permissions_set',
        related_query_name='user',
    )

    USERNAME_FIELD = 'email'


    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
