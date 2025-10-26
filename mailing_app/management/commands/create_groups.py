from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from mailing_app.models import Client, Message, Mailing

MODELS_WITH_PERMISSIONS = [Client, Message, Mailing]
GROUP_NAME = 'Менеджеры'


class Command(BaseCommand):
    """
    Кастомная команда для создания группы "Менеджеры" (Критерий 5.4)
    и автоматического назначения ей всех кастомных прав, определенных в Meta классах моделей.
    """
    help = f'Создает группу "{GROUP_NAME}" и назначает ей кастомные права.'

    def handle(self, *args, **options):
        manager_group, created = Group.objects.get_or_create(name=GROUP_NAME)

        if created:
            self.stdout.write(self.style.SUCCESS(f'Группа "{GROUP_NAME}" успешно создана.'))
        else:
            self.stdout.write(self.style.WARNING(f'Группа "{GROUP_NAME}" уже существует.'))
            manager_group.permissions.clear()
            self.stdout.write(self.style.WARNING(f'Существующие права группы "{GROUP_NAME}" очищены.'))

        custom_permissions = []
        for model in MODELS_WITH_PERMISSIONS:
            content_type = ContentType.objects.get_for_model(model)

            if hasattr(model._meta, 'permissions'):
                for codename, name in model._meta.permissions:
                    try:
                        permission = Permission.objects.get(
                            codename=codename,
                            content_type=content_type
                        )
                        custom_permissions.append(permission)
                    except Permission.DoesNotExist:
                        self.stdout.write(
                            self.style.ERROR(f"Право '{codename}' для модели {model._meta.model_name} не найдено. "
                                             f"Выполните 'python manage.py migrate' для его создания.")
                        )

        if custom_permissions:
            manager_group.permissions.set(custom_permissions)
            self.stdout.write(self.style.SUCCESS(
                f'Группе "{GROUP_NAME}" назначено {len(custom_permissions)} кастомных прав.'
            ))
        else:
            self.stdout.write(self.style.WARNING('Не найдено кастомных прав для назначения.'))
