from django.contrib.auth.forms import UserChangeForm
from .models import User

class UserProfileForm(UserChangeForm):
    """Форма для редактирования профиля пользователя."""
    class Meta:
        model = User
        fields = ('email', 'avatar', 'phone', 'country')
        exclude = ('password', 'last_login', 'is_superuser', 'is_staff', 'is_active', 'date_joined', 'groups', 'user_permissions')

    def __init__(self, *args, **kwargs):
        """Переопределение для удаления поля пароля, которое добавляется по умолчанию."""
        super().__init__(*args, **kwargs)
        if 'password' in self.fields:
            del self.fields['password']
