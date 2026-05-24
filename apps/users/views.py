from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import LoginAuthenticationForm, UserRegistrationForm

class CustomLoginView(LoginView):
    authentication_form = LoginAuthenticationForm
    template_name = 'users/login.html'
    redirect_authenticated_user = True

class RegisterView(CreateView):
    form_class = UserRegistrationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        messages.success(self.request, 'Регистрация успешна! Войдите в систему.')
        return super().form_valid(form)
    
class CustomLogoutView(LogoutView):
    next_page = 'users:login' 



