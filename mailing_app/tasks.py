from celery import shared_task
from django.utils import timezone
from .models import Mailing
from .services import send_mailing_messages

@shared_task
def send_scheduled_mailings():
    now = timezone.now()
    active_mailings = Mailing.objects.filter(
        start_date__lte=now.date(),
        end_date__gte=now.date(),
        status__in=['created', 'started']
    )

    for mailing in active_mailings:
        # Логика для определения, нужно ли запускать рассылку сейчас
        last_attempt = mailing.mailingattempt_set.order_by('-timestamp').first()
        should_send = False

        if not last_attempt:
            # Если это первая попытка, отправляем, если время пришло
            if mailing.start_time.hour == now.hour and mailing.start_time.minute == now.minute:
                should_send = True
        else:
            # Логика для ежедневных, еженедельных и ежемесячных рассылок
            if mailing.frequency == 'daily':
                if (now - last_attempt.timestamp).days >= 1:
                    should_send = True
            elif mailing.frequency == 'weekly':
                if (now - last_attempt.timestamp).days >= 7:
                    should_send = True
            elif mailing.frequency == 'monthly':
                # Примерная логика для ежемесячной
                if (now.month != last_attempt.timestamp.month) or \
                   ((now - last_attempt.timestamp).days >= 28 and now.day == last_attempt.timestamp.day):
                    should_send = True

        if should_send:
            send_mailing_messages(mailing.id)
