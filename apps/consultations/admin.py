from django.contrib import admin
from .models import Consultation

@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):
    list_display = ('user', 'datetime_create')
    search_fields = ('question', 'answer')
    readonly_fields = ('datetime_create', 'question', 'answer', 'user')