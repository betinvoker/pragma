from django.db import models

# ==========================================
# Документ (DOCUMENT)
# ==========================================
class DocType(models.TextChoices):
    INVOICE = 'INV', 'Счет-фактура'
    CONTRACT = 'CTR', 'Договор'
    AGREEMENT = 'AGR', 'Соглашение'

class Document(models.Model):
    title = models.CharField('Заголовок', max_length=256)
    doc_type = models.CharField('Тип документа', max_length=3, choices=DocType.choices)
    description = models.TextField('Описание', max_length=5096, null=True, blank=True)
    version = models.IntegerField('Версия', default=1)
    link_file = models.CharField('Ссылка на документ', max_length=2048, null=True, blank=True)
    order = models.ForeignKey('orders.Order', on_delete=models.CASCADE, related_name='documents', verbose_name='Заказ')
    datetime_create = models.DateTimeField('Дата создания', auto_now_add=True)
    datetime_update = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        db_table = 'document'
        verbose_name = 'Документ'
        verbose_name_plural = 'Документы'

    def __str__(self):
        return f"{self.title} ({self.doc_type}) v{self.version}"