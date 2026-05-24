from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Order

@login_required
def client_orders(request):
    orders = Order.objects.filter(client=request.user).prefetch_related('items__item', 'documents')
    return render(request, 'orders/client_list.html', {'orders': orders})

@login_required
def manager_orders(request):
    orders = Order.objects.all().prefetch_related('items__item', 'documents').select_related('client', 'manager')
    return render(request, 'orders/manager_list.html', {'orders': orders})

@login_required
def manager_order_detail(request, pk):
    order = get_object_or_404(Order.objects.prefetch_related('items__item', 'documents').select_related('client', 'manager'), pk=pk)
    return render(request, 'orders/manager_detail.html', {'order': order})