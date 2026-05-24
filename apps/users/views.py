from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from django.db import models
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


@login_required
def client_profile(request):
    from .forms import UserProfileForm
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль успешно обновлён')
            return redirect('home')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'users/profile.html', {'form': form})


@login_required
def manager_profile(request):
    from .forms import UserProfileForm
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль успешно обновлён')
            return redirect('home')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'users/manager_profile.html', {'form': form})


@login_required
def manager_users(request):
    from .models import User
    clients = User.objects.filter(role=1)
    q = request.GET.get('q', '')
    if q:
        clients = clients.filter(last_name__icontains=q) | clients.filter(first_name__icontains=q) | clients.filter(company__icontains=q) | clients.filter(phone__icontains=q)
    return render(request, 'users/manager_users.html', {'clients': clients, 'q': q})


@login_required
def manager_user_detail(request, pk):
    from .models import User
    from apps.orders.models import Order
    user = User.objects.get(pk=pk)
    orders = Order.objects.filter(client=user)
    return render(request, 'users/manager_user_detail.html', {'client': user, 'orders': orders})


@login_required
def manager_analytics(request):
    from .models import User
    from apps.orders.models import Order
    from apps.catalog.models import Item
    clients_count = User.objects.filter(role=1).count()
    items_count = Item.objects.count()
    orders_count = Order.objects.count()
    avg = Order.objects.aggregate(avg=models.Avg('total_amount'))['avg'] or 0
    top_clients = User.objects.filter(role=1, client_orders__isnull=False).annotate(order_count=models.Count('client_orders')).order_by('-order_count')[:10]
    top_avg = User.objects.filter(role=1, client_orders__isnull=False).annotate(avg_order=models.Avg('client_orders__total_amount')).order_by('-avg_order')[:10]
    return render(request, 'orders/analytics.html', {'data': {
        'clients': clients_count,
        'catalog_items': items_count,
        'orders': orders_count,
        'avg_check': avg,
        'top_by_orders': top_clients,
        'top_by_avg_check': top_avg,
    }}) 



