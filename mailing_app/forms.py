from django import forms
from .models import Client, Message, Mailing

class ClientForm(forms.ModelForm):
    """Форма для создания и редактирования Клиентов."""
    class Meta:
        model = Client
        fields = ('email', 'full_name', 'comment')

class MessageForm(forms.ModelForm):
    """Форма для создания и редактирования Сообщений."""
    class Meta:
        model = Message
        fields = ('subject', 'body')

class MailingForm(forms.ModelForm):
    """Форма для создания и редактирования Рассылок."""
    class Meta:
        model = Mailing
        fields = ('start_date', 'start_time', 'end_date', 'frequency', 'message', 'clients')
