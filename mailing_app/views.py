from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .models import Client, Message, Mailing, MailingAttempt
from .forms import ClientForm, MessageForm, MailingForm
from .services import send_mailing_messages

@login_required
def home_view(request):
    """
    Контроллер для отображения главной страницы.
    Предоставляет статистику по рассылкам текущего пользователя.
    """
    total_mailings = Mailing.objects.filter(owner=request.user).count()
    active_mailings = Mailing.objects.filter(owner=request.user, status='started').count()
    unique_clients = Client.objects.filter(owner=request.user).distinct().count()

    context = {
        'total_mailings': total_mailings,
        'active_mailings': active_mailings,
        'unique_clients': unique_clients
    }
    return render(request, 'mailing_app/home.html', context)

@login_required
def mailing_send_now(request, pk):
    """
    Контроллер для немедленной отправки рассылки (Критерий 7.2).
    Вызывает сервис отправки, а затем перенаправляет на список рассылок.
    """
    send_mailing_messages(pk)
    return redirect(reverse('mailing_app:mailing_list'))

# --- CRUD Клиентов ---

class ClientListView(LoginRequiredMixin, ListView):
    """Отображает список клиентов (Критерий 5.8). Требует авторизации."""
    model = Client
    template_name = 'mailing_app/client_list.html'
    context_object_name = 'clients'

    def get_queryset(self):
        """Фильтрация списка клиентов по текущему пользователю (владельцу)."""
        return Client.objects.filter(owner=self.request.user)

class ClientCreateView(LoginRequiredMixin, CreateView):
    """Создание нового клиента."""
    model = Client
    form_class = ClientForm
    template_name = 'mailing_app/client_form.html'
    success_url = reverse_lazy('mailing_app:client_list')

    def form_valid(self, form):
        """Автоматически устанавливает текущего пользователя как владельца."""
        form.instance.owner = self.request.user
        return super().form_valid(form)

class ClientDetailView(LoginRequiredMixin, DetailView):
    """Просмотр деталей клиента."""
    model = Client
    template_name = 'mailing_app/client_detail.html'

class ClientUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирование клиента."""
    model = Client
    form_class = ClientForm
    template_name = 'mailing_app/client_form.html'
    success_url = reverse_lazy('mailing_app:client_list')

class ClientDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление клиента."""
    model = Client
    template_name = 'mailing_app/client_confirm_delete.html'
    success_url = reverse_lazy('mailing_app:client_list')

    # --- CRUD Сообщений ---

class MessageListView(LoginRequiredMixin, ListView):
    """Отображает список сообщений. Требует авторизации."""
    model = Message
    template_name = 'mailing_app/message_list.html'
    context_object_name = 'messages'

    def get_queryset(self):
        """Фильтрация списка сообщений по текущему пользователю (владельцу)."""
        return Message.objects.filter(owner=self.request.user)

class MessageCreateView(LoginRequiredMixin, CreateView):
    """Создание нового сообщения."""
    model = Message
    form_class = MessageForm
    template_name = 'mailing_app/message_form.html'
    success_url = reverse_lazy('mailing_app:message_list')

    def form_valid(self, form):
        """Автоматически устанавливает текущего пользователя как владельца."""
        form.instance.owner = self.request.user
        return super().form_valid(form)

class MessageDetailView(LoginRequiredMixin, DetailView):
    """Просмотр деталей сообщения."""
    model = Message
    template_name = 'mailing_app/message_detail.html'

class MessageUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирование сообщения."""
    model = Message
    form_class = MessageForm
    template_name = 'mailing_app/message_form.html'
    success_url = reverse_lazy('mailing_app:message_list')

class MessageDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление сообщения."""
    model = Message
    template_name = 'mailing_app/message_confirm_delete.html'
    success_url = reverse_lazy('mailing_app:message_list')

    # --- CRUD Рассылок ---

class MailingListView(LoginRequiredMixin, ListView):
    """Отображает список рассылок. Требует авторизации."""
    model = Mailing
    template_name = 'mailing_app/mailing_list.html'
    context_object_name = 'mailings'

    def get_queryset(self):
        """Фильтрация списка рассылок по текущему пользователю (владельцу)."""
        return Mailing.objects.filter(owner=self.request.user)

class MailingCreateView(LoginRequiredMixin, CreateView):
    """Создание новой рассылки."""
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing_app/mailing_form.html'
    success_url = reverse_lazy('mailing_app:mailing_list')

    def form_valid(self, form):
        """Автоматически устанавливает текущего пользователя как владельца."""
        form.instance.owner = self.request.user
        return super().form_valid(form)

class MailingDetailView(LoginRequiredMixin, DetailView):
    """Просмотр деталей рассылки."""
    model = Mailing
    template_name = 'mailing_app/mailing_detail.html'

class MailingUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирование рассылки."""
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing_app/mailing_form.html'
    success_url = reverse_lazy('mailing_app:mailing_list')

class MailingDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление рассылки."""
    model = Mailing
    template_name = 'mailing_app/mailing_confirm_delete.html'
    success_url = reverse_lazy('mailing_app:mailing_list')

class MailingAttemptListView(LoginRequiredMixin, ListView):
    """
    Отображает список попыток отправки.
    Фильтрует по рассылкам, владельцем которых является текущий пользователь.
    """
    model = MailingAttempt
    template_name = 'mailing_app/mailingattempt_list.html'
    context_object_name = 'attempts'

    def get_queryset(self):
        """Фильтрация попыток по владельцу рассылки."""
        # Используем двойное подчеркивание для фильтрации по полю owner в связанной модели Mailing
        return MailingAttempt.objects.filter(mailing__owner=self.request.user).order_by('-timestamp')
