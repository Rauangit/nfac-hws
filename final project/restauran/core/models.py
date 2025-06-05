from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import models
from django.contrib.auth import get_user_model

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'admin', 'Админ (приемщик)'

        CHEF = 'chef', 'Повар'
        CLIENT = 'client', 'Клиент'

        
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.CLIENT,
    )

    phone_number = models.CharField(max_length=20, blank=True, null=True)
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    preparation_time = models.DurationField(help_text="Пример: 00:30:00 для 30 минут")
    price = models.DecimalField(max_digits=6, decimal_places=2)
    is_in_stop_list = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ({'стоп' if self.is_in_stop_list else 'в наличии'})"


class CardInfo(models.Model):
    client = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    card_number = models.CharField(max_length=16)  
    expiry_date = models.CharField(max_length=5)  
    cardholder_name = models.CharField(max_length=100)
    cvv = models.CharField(max_length=3)
    def __str__(self):

        return f"Карта {self.card_number[-4:]} для {self.client.username}"

class Table(models.Model):
    number = models.PositiveIntegerField(unique=True)  
    capacity = models.PositiveIntegerField()  
    is_available = models.BooleanField(default=True)  

    def __str__(self):
        return f"Стол #{self.number} ({'свободен' if self.is_available else 'занят'})"


class TableBooking(models.Model):
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    table = models.ForeignKey(Table, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateField()
    time = models.TimeField()
    number_of_people = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=[
        ('booked', 'Забронировано'),
        ('cancelled', 'Отменено'),
        ('seated', 'Посажен'),
    ], default='booked')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.client.username} | {self.date} {self.time} — Стол #{self.table.number if self.table else 'не выбран'} ({self.status})"
    
class Order(models.Model):
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    # Разрешаем NULL и blank
    booking = models.ForeignKey(
        TableBooking,
        on_delete=models.SET_NULL,  # безопаснее, чем CASCADE
        null=True,
        blank=True,
        related_name="orders"
    )

    items = models.ManyToManyField(MenuItem)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'В ожидании'),
        ('preparing', 'Готовится'),
        ('done', 'Готово'),
    ], default='pending')

    def __str__(self):
        return f"Заказ {self.id} от {self.client.username} ({self.status})"


@login_required
def add_to_order(request, item_id):
    user = request.user
    item = get_object_or_404(MenuItem, id=item_id)

    # Попытаемся найти текущий активный заказ клиента (pending)
    order = Order.objects.filter(client=user, status='pending').order_by('-created_at').first()

    if not order:
        # Пробуем найти последнюю бронь (если есть), но это не обязательно
        booking = TableBooking.objects.filter(client=user, status='booked').order_by('-date', '-time').first()
        
        # Создаём заказ: даже если booking=None — это ОК
        order = Order.objects.create(client=user, booking=booking)

        if not booking:
            messages.warning(request, "У вас нет брони. Заказ создан без привязки к столу.")

    # Добавляем блюдо
    order.items.add(item)
    order.save()

    messages.success(request, f"Блюдо '{item.name}' добавлено в ваш заказ.")
    return redirect('client_home')

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')  # <-- related_name добавлен
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

class BookingRequest(models.Model):
    client = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    number_of_people = models.PositiveIntegerField()
    status = models.CharField(max_length=20, default='new')  # new, accepted, rejected
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Заявка от {self.client} на стол {self.table} {self.date} {self.time}"