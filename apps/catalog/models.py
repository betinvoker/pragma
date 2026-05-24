from django.db import models

# ==========================================
# Товар (ITEM)
# ==========================================
class Item(models.Model):
    name = models.CharField('Наименование', max_length=256)
    description = models.TextField('Описание', max_length=5096, null=True, blank=True)
    price = models.DecimalField('Цена', max_digits=12, decimal_places=2)
    stock = models.IntegerField('Количество на складе')
    link_image = models.CharField('Ссылка на изображение', max_length=2048, null=True, blank=True)
    datetime_create = models.DateTimeField('Дата создания', auto_now_add=True)
    datetime_update = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        db_table = 'item'
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name