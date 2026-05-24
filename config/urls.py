from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.catalog.models import Item
from apps.catalog.views import catalog_list, manager_catalog, client_cart, cart_add, cart_remove
from apps.orders.views import client_orders, manager_orders, manager_order_detail
from apps.documents.views import client_documents, manager_documents
from apps.consultations.views import client_ai
from apps.users.views import client_profile, manager_profile, manager_users, manager_user_detail, manager_analytics


@login_required
def home(request):
    catalog = Item.objects.all()[:6]
    return render(request, 'home.html', {'catalog': catalog})


urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('apps.users.urls', namespace='users')),
    path('', home, name='home'),

    path('client/', home, name='client_dashboard'),
    path('client/catalog/', catalog_list, name='client_catalog'),
    path('client/cart/', client_cart, name='client_cart'),
    path('client/cart/add/', cart_add, name='client_cart_add'),
    path('client/cart/remove/', cart_remove, name='client_cart_remove'),
    path('client/orders/', client_orders, name='client_orders'),
    path('client/documents/', client_documents, name='client_documents'),
    path('client/profile/', client_profile, name='client_profile'),
    path('client/ai/', client_ai, name='client_ai'),

    path('manager/', home, name='manager_dashboard'),
    path('manager/catalog/', manager_catalog, name='manager_catalog'),
    path('manager/orders/', manager_orders, name='manager_orders'),
    path('manager/order/<int:pk>/', manager_order_detail, name='manager_order_detail'),
    path('manager/users/', manager_users, name='manager_users'),
    path('manager/user/<int:pk>/', manager_user_detail, name='manager_user_detail'),
    path('manager/documents/', manager_documents, name='manager_documents'),
    path('manager/analytics/', manager_analytics, name='manager_analytics'),
    path('manager/profile/', manager_profile, name='manager_profile'),
]