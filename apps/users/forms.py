from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate
from .models import User

class LoginAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label='Логин',
        widget=forms.TextInput(attrs={
            'autofocus': True, 
            'class': 'form-control',
            'placeholder': 'Введите логин',
        })
    )

    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль',
        })
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
    
class UserRegistrationForm(UserCreationForm):
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль'
        })
    )
    password2 = forms.CharField(
        label='Подтверждение пароля',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Повторите пароль'
        })
    )
    
    class Meta:
        model = User
        fields = ('login', 'first_name', 'last_name', 'patronymic', 'company', 'phone', 'email', 'password1', 'password2')
        widgets = {
            'login': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Придумайте логин'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Фамилия'}),
            'patronymic': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Отчество'}),
            'company': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название компании'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+7 (999) 123-45-67'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@email.email'}),
        }
        
    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = User.Role.CLIENT
        if commit:
            user.save()
        return user