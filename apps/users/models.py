from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

# ==========================================
# Кастомная модель пользователя
# ==========================================
class UserManager(BaseUserManager):
    def create_user(self, login, password=None, **extra_fields):
        if not login:
            raise ValueError('Поле login обязательно')
        user = self.model(login=login, **extra_fields)
        user.set_password(password)  # Хеширует пароль (pbkdf2_sha256 по умолчанию в Django)
        user.save(using=self._db)
        return user

    def create_superuser(self, login, password=None, **extra_fields):
        extra_fields.setdefault('role', User.Role.ADMIN)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(login, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    # Атрибуты из таблицы USER
    login = models.CharField('Логин', max_length=150, unique=True)
    last_name = models.CharField('Фамилия', max_length=100)
    first_name = models.CharField('Имя', max_length=100)
    patronymic = models.CharField('Отчество', max_length=100, null=True, blank=True)
    company = models.CharField('Название компании', max_length=255, null=True, blank=True)
    phone = models.CharField('Номер телефона', max_length=50)
    email = models.EmailField('Электронная почта', max_length=512, null=True, blank=True)
    
    class Role(models.IntegerChoices):
        CLIENT = 1, 'Клиент'
        MANAGER = 2, 'Менеджер'
        ADMIN = 3, 'Администратор'
    
    role = models.PositiveSmallIntegerField('Роль', choices=Role.choices)
    jur_address = models.CharField('Юридический адрес', max_length=1024, null=True, blank=True)
    datetime_create = models.DateTimeField('Дата регистрации', auto_now_add=True)
    
    # Обязательные поля для работы Django Admin
    is_active = models.BooleanField('Активен', default=True)
    is_staff = models.BooleanField('Доступ в админку', default=False)

    objects = UserManager()

    USERNAME_FIELD = 'login'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone']

    class Meta:
        db_table = 'user'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f"{self.last_name} {self.first_name} ({self.login})"