from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Document
from apps.orders.models import Order

@login_required
def client_documents(request):
    orders = Order.objects.filter(client=request.user)
    documents = Document.objects.filter(order__in=orders)
    search = request.GET.get('search', '')
    if search:
        documents = documents.filter(title__icontains=search)
    return render(request, 'documents/client_list.html', {'documents': documents, 'search': search})

@login_required
def manager_documents(request):
    documents = Document.objects.all().select_related('order')
    search = request.GET.get('search', '')
    if search:
        documents = documents.filter(title__icontains=search)
    orders = Order.objects.all()
    return render(request, 'documents/manager_list.html', {'documents': documents, 'orders': orders, 'search': search})