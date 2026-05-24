from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
from .forms import LoginAuthenticationForm

# Создаём экземпляр кастомного админ-сайта
admin.site.login_form = LoginAuthenticationForm

# Регистрируем модели в нашем админ-сайте
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # Список: добавляем метод для отображения роли текстом
    list_display = ('login', 'last_name', 'first_name', 'email', 'phone', 'get_role_display', 'is_active', 'is_staff', 'datetime_create')
    
    # Фильтры
    list_filter = ('role', 'is_active', 'is_staff', 'is_superuser', 'datetime_create')
    
    # Поиск
    search_fields = ('login', 'first_name', 'last_name', 'email', 'phone', 'company')
    
    # Сортировка
    ordering = ('-datetime_create',)
    
    # Быстрое редактирование статуса
    list_editable = ('is_active',)
    
    # Группировка полей
    fieldsets = (
        (None, {'fields': ('login', 'password')}),
        ('Персональные данные', {'fields': ('first_name', 'last_name', 'patronymic', 'email', 'phone')}),
        ('Компания', {'fields': ('company', 'jur_address'), 'classes': ('collapse',)}),
        ('Права доступа', {'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Даты', {'fields': ('last_login', 'datetime_create'), 'classes': ('collapse',)}),
    )
    
    # Форма создания
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('login', 'password1', 'password2', 'first_name', 'last_name', 'phone', 'email', 'role', 'is_active', 'is_staff'),
        }),
    )
    
    # Только для чтения
    readonly_fields = ('last_login', 'datetime_create')

    # Метод для отображения роли текстом вместо цифры
    @admin.display(description='Роль', ordering='role')
    def get_role_display(self, obj):
        return obj.get_role_display()