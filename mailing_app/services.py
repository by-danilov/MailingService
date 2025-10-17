from django.core.mail import send_mail
from django.conf import settings
from .models import Mailing, MailingAttempt


def send_mailing_messages(mailing_id):
    """
    Отправляет email-сообщения по указанной рассылке и записывает результат в лог (MailingAttempt).

    Args:
        mailing_id (int): ID объекта Mailing, который нужно отправить.

    Returns:
        bool: True, если отправка и логирование прошли успешно, иначе False.
    """
    try:
        mailing = Mailing.objects.get(id=mailing_id)
        if mailing.status == 'created':
            mailing.status = 'started'
            mailing.save()

        clients = mailing.clients.all()
        recipients = [client.email for client in clients]
        subject = mailing.message.subject
        body = mailing.message.body

        response = send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            recipients,
            fail_silently=False
        )

        status = 'success' if response else 'failed'
        server_response = 'Successfully sent.' if response else 'Failed to send.'

        MailingAttempt.objects.create(
            mailing=mailing,
            status=status,
            server_response=server_response
        )

        return True

    except Exception as e:
        MailingAttempt.objects.create(
            mailing=mailing,
            status='failed',
            server_response=str(e)
        )
        return False
