from django.db import models

# ==========================================
# Заказ (ORDER)
# ==========================================
class OrderStatus(models.TextChoices):
    ERROR = '0', 'Ошибка'
    NEW = '1', 'Новый'
    REGISTERED = '2', 'Зарегистрирован'
    IN_PROGRESS = '3', 'В работе'
    COMPLETED = '4', 'Завершен'
    CANCELLED = '5', 'Отменен'

class Order(models.Model):
    client = models.ForeignKey(
        'users.User', on_delete=models.CASCADE, related_name='client_orders',
        limit_choices_to={'role': 1}, verbose_name='Клиент'
    )
    manager = models.ForeignKey(
        'users.User', on_delete=models.CASCADE, related_name='manager_orders',
        limit_choices_to={'role': 2}, verbose_name='Менеджер'
    )
    status = models.CharField('Статус', max_length=1, choices=OrderStatus.choices, default=OrderStatus.NEW)
    total_amount = models.DecimalField('Общая сумма', max_digits=12, decimal_places=2)
    datetime_create = models.DateTimeField('Дата создания', auto_now_add=True)
    datetime_update = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        db_table = 'order'
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-datetime_create']

    def __str__(self):
        return f"Заказ #{self.pk} от {self.client}"

class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Заказ'
    )
    item = models.ForeignKey(
        'catalog.Item',
        on_delete=models.CASCADE,
        related_name='order_items',
        verbose_name='Товар'
    )
    quantity = models.IntegerField('Количество', default=1)
    price = models.DecimalField(
        'Итоговая стоимость',
        max_digits=12,
        decimal_places=2
    )

    class Meta:
        db_table = 'order_item'
        verbose_name = 'Элемент заказа'
        verbose_name_plural = 'Элементы заказа'
        unique_together = ('order', 'item')

    def __str__(self):
        return f"{self.quantity}x {self.item.name} в заказе #{self.order_id}"