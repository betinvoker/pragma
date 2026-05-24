from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from .models import User


class LoginAuthenticationForm(AuthenticationForm):
    """Форма входа, использующая поле 'login' вместо 'username'"""
    
    username = forms.CharField(
        label='Логин',
        widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'})
    )
    
    def clean(self):
        login = self.cleaned_data.get('username')  # в форме поле называется username, но это наш login
        password = self.cleaned_data.get('password')
        
        if login and password:
            # authenticate() автоматически использует USERNAME_FIELD из модели
            self.user = authenticate(
                request=self.request,
                login=login,  # передаём как 'login', потому что USERNAME_FIELD = 'login'
                password=password
            )
            if self.user is None:
                raise forms.ValidationError(
                    'Неверный логин или пароль',
                    code='invalid_login',
                )
        return super().clean()
    
    def get_user(self):
        return getattr(self, 'user', None)