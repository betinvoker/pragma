from django.contrib import admin
from .models import Document

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'doc_type', 'order', 'version', 'datetime_create')
    list_filter = ('doc_type',)
    search_fields = ('title', 'description')
    readonly_fields = ('datetime_create', 'datetime_update')