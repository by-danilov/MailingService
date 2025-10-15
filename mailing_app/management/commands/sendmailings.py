from django.core.management.base import BaseCommand
from mailing_app.tasks import send_scheduled_mailings
from django.conf import settings


class Command(BaseCommand):
    help = 'Запускает Celery-задачу для обработки всех запланированных рассылок.'

    def handle(self, *args, **options):
        if not settings.CELERY_BROKER_URL:
            self.stdout.write(self.style.ERROR('CELERY_BROKER_URL не настроен в .env. Запуск рассылок невозможен.'))
            return

        self.stdout.write(self.style.SUCCESS('Инициирую запуск запланированных рассылок через Celery...'))

        try:
            send_scheduled_mailings.delay()
            self.stdout.write(
                self.style.SUCCESS('Задача успешно отправлена в Celery. Проверьте логи Celery Worker для деталей.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ошибка при отправке задачи в Celery: {e}'))
