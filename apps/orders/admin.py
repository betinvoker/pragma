from django.contrib import admin
from .models import Order, OrderItem

# Регистрация остальных моделей в стандартном admin.site
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'manager', 'status', 'total_amount', 'datetime_create')
    list_filter = ('status', 'datetime_create')
    search_fields = ('client__login', 'manager__login')
    readonly_fields = ('datetime_create', 'datetime_update')

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'item', 'quantity', 'price')
    list_filter = ('order',)
    readonly_fields = ('price',)
