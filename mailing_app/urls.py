from django.urls import path
from .views import (
    home_view,
    ClientListView, ClientCreateView, ClientDetailView, ClientUpdateView, ClientDeleteView,
    MessageListView, MessageCreateView, MessageDetailView, MessageUpdateView, MessageDeleteView,
    MailingListView, MailingCreateView, MailingDetailView, MailingUpdateView, MailingDeleteView,
    MailingAttemptListView,
    mailing_send_now,
)

app_name = 'mailing_app'

urlpatterns = [
    # ГЛАВНАЯ СТРАНИЦА И ЛОГИ
    path('', home_view, name='home'),
    path('attempts/', MailingAttemptListView.as_view(), name='attempt_list'),
    path('send/<int:pk>/', mailing_send_now, name='mailing_send_now'),

    # КЛИЕНТЫ
    path('clients/', ClientListView.as_view(), name='client_list'),
    path('clients/create/', ClientCreateView.as_view(), name='client_create'),
    path('clients/<int:pk>/', ClientDetailView.as_view(), name='client_detail'),
    path('clients/<int:pk>/update/', ClientUpdateView.as_view(), name='client_update'),
    path('clients/<int:pk>/delete/', ClientDeleteView.as_view(), name='client_delete'),

    # СООБЩЕНИЯ
    path('messages/', MessageListView.as_view(), name='message_list'),
    path('messages/create/', MessageCreateView.as_view(), name='message_create'),
    path('messages/<int:pk>/', MessageDetailView.as_view(), name='message_detail'),
    path('messages/<int:pk>/update/', MessageUpdateView.as_view(), name='message_update'),
    path('messages/<int:pk>/delete/', MessageDeleteView.as_view(), name='message_delete'),

    # РАССЫЛКИ
    path('mailings/', MailingListView.as_view(), name='mailing_list'),
    path('mailings/create/', MailingCreateView.as_view(), name='mailing_create'),
    path('mailings/<int:pk>/', MailingDetailView.as_view(), name='mailing_detail'),
    path('mailings/<int:pk>/update/', MailingUpdateView.as_view(), name='mailing_update'),
    path('mailings/<int:pk>/delete/', MailingDeleteView.as_view(), name='mailing_delete'),
]
