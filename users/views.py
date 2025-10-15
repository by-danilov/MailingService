from django.views.generic import DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import User
from .forms import UserProfileForm


class ProfileDetailView(LoginRequiredMixin, DetailView):
    """
    Просмотр профиля текущего пользователя (Критерий 3.4).
    Доступен только авторизованным пользователям.
    """
    model = User
    template_name = 'users/profile_detail.html'

    def get_object(self, queryset=None):
        return self.request.user


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """
    Редактирование профиля текущего пользователя (Критерий 3.5).
    Доступен только авторизованным пользователям.
    """
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile_form.html'
    success_url = reverse_lazy('users:profile_detail')

    def get_object(self, queryset=None):
        return self.request.user
