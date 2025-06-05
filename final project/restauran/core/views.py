from django.shortcuts import render, redirect,get_object_or_404
from .forms import ClientRegistrationForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import date
from .models import MenuItem, Table, TableBooking, Order
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from .models import OrderItem
from .forms import ClientBookingForm
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import MenuItemForm
from django.shortcuts import render, redirect, get_object_or_404
from .models import MenuItem, Order
from django.views.decorators.http import require_http_methods
from .models import TableBooking, Order  # или как у тебя называются модели

@login_required
def my_bookings_view(request):
    # Получаем активные брони пользователя
    bookings = TableBooking.objects.filter(client=request.user)

    # Получаем все заказы пользователя
    menu_orders = Order.objects.filter(client=request.user)

    context = {
        'bookings': bookings,
        'menu_orders': menu_orders
    }
    return render(request, 'client/my_bookings.html', context)


@login_required
def client_dashboard_view(request):
    return render(request, 'client/dashboard.html')

@login_required
def make_order_view(request):
    # Проверяем, есть ли активная бронь
    booking = TableBooking.objects.filter(client=request.user, status='approved').last()

    if request.method == 'POST':
        form = Order(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.client = request.user
            if booking:
                order.booking = booking  # Привязываем заказ к брони, если есть
            order.save()
            form.save_m2m()
            messages.success(request, "Ваш заказ успешно создан.")
            return redirect('client_home')
    else:
        form = Order()

    if not booking:
        messages.warning(request, "У вас нет забронированного стола. Заказ будет оформлен, но без брони.")

    return render(request, 'core/make_order.html', {
        'form': form,
        'booking': booking,
    })

@login_required
def book_table_view(request):
    if request.method == 'POST':
        form = ClientBookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.client = request.user
            booking.status = 'pending'  # или как у тебя предусмотрено
            booking.save()
            messages.success(request, "Заявка на бронь отправлена.")
            return redirect('client_home')
    else:
        form = ClientBookingForm()

    return render(request, 'core/book_table.html', {'form': form})

def menu_view(request):
    menu_items = MenuItem.objects.filter(is_in_stop_list=False)  # показываем только доступные блюда
    return render(request, 'client/menu.html', {'menu_items': menu_items})

def available_tables_view(request):
    tables = Table.objects.filter(is_available=True)
    return render(request, 'core/available_tables.html', {'tables': tables})

@login_required
def menu_order_view(request, booking_id):
    # Получаем бронь по ID, убеждаемся, что она принадлежит текущему пользователю (если клиент)
    booking = get_object_or_404(TableBooking, id=booking_id)

    # Получаем все заказы, связанные с этой бронью
    orders = Order.objects.filter(booking=booking)

    # Для простоты — берем первый активный заказ со статусом 'pending', если есть
    active_order = orders.filter(status='pending').first()

    # Если заказа пока нет, то можно показать пустой список блюд или предлагать добавить
    items_in_order = active_order.items.all() if active_order else []

    context = {
        'booking': booking,
        'order': active_order,
        'items': items_in_order,
    }

    return render(request, 'client/menu_order.html', context)

@login_required
def client_bookings_view(request):
    bookings = TableBooking.objects.filter(client=request.user)
    return render(request, 'client/my_bookings.html', {'bookings': bookings})
def is_chef(user):
    return user.is_authenticated and user.role == 'chef'

@login_required
@user_passes_test(is_chef)
def chef_dashboard(request):
    orders = Order.objects.select_related('client', 'booking').prefetch_related('items')
    menu_items = MenuItem.objects.all()

    if request.method == 'POST':
        # Смена статуса заказа
        if 'change_order_status' in request.POST:
            order_id = request.POST.get('order_id')
            new_status = request.POST.get('new_status')
            order = get_object_or_404(Order, id=order_id)
            order.status = new_status
            order.save()
            messages.success(request, f"Статус заказа #{order_id} изменён на {order.get_status_display()}")
            return redirect('chef_dashboard')

        # Добавление нового блюда
        if 'add_menu_item' in request.POST:
            form = MenuItemForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Новое блюдо добавлено.")
                return redirect('chef_dashboard')
            else:
                messages.error(request, "Ошибка при добавлении блюда.")
        else:
            form = MenuItemForm(request.POST)

        # Стоп-лист
        if 'toggle_stop_list' in request.POST:
            item_id = request.POST.get('item_id')
            item = get_object_or_404(MenuItem, id=item_id)
            item.is_in_stop_list = not item.is_in_stop_list
            item.save()
            status_text = "в стоп-листе" if item.is_in_stop_list else "снято с стоп-листа"
            messages.success(request, f"Блюдо '{item.name}' теперь {status_text}.")
            return redirect('chef_dashboard')
    else:
        form = MenuItemForm()

    context = {
        'orders': orders,
        'menu_items': menu_items,
        'form': form,
    }
    return render(request, 'core/chef_dashboard.html', context)

@staff_member_required
def admin_dashboard(request):
    tab = request.GET.get("tab", "bookings")
    today = date.today()
    context = {
        "tab": tab,
        "today": today,
        "date": today,
    }

    # Переключение статуса стола
    if request.method == 'POST' and tab == 'tables':
        if "toggle_table_status" in request.POST:
            table_id = request.POST.get("table_id")
            table = Table.objects.filter(id=table_id).first()
            if table:
                table.is_available = not table.is_available
                table.save()
                messages.success(request, f"Статус стола №{table.number} изменён на {'свободен' if table.is_available else 'занят'}.")
            else:
                messages.error(request, "Стол не найден.")
            return redirect('/admin-dashboard/?tab=tables')

        # Логика создания брони (если нужна)
        if "create_booking" in request.POST:
            # твой код создания брони
            pass

    if tab == "bookings":
        bookings = TableBooking.objects.filter(date=today, status="booked").order_by('time')
        pending_bookings = TableBooking.objects.filter(date__gte=today, status="pending").order_by('date', 'time')
        context["bookings"] = bookings
        context["pending_bookings"] = pending_bookings

    elif tab == "orders":
        orders = Order.objects.select_related("booking", "client").prefetch_related("items")
        context["orders"] = orders

    elif tab == "tables":
        tables = Table.objects.all()
        clients = get_user_model().objects.filter(is_staff=False)
        context["tables"] = tables
        context["clients"] = clients

        if request.method == 'POST' and "create_booking" in request.POST:
            table_id = request.POST.get("table_id")
            client_id = request.POST.get("client_id")
            date_val = request.POST.get("date")
            time_val = request.POST.get("time")
            number = request.POST.get("number_of_people")
            if table_id and client_id:
                TableBooking.objects.create(
                    table_id=table_id,
                    client_id=client_id,
                    date=date_val,
                    time=time_val,
                    number_of_people=number,
                    status="booked"
                )
                messages.success(request, "Бронирование успешно создано!")
                return redirect("/admin-dashboard/?tab=tables")

    return render(request, "core/admin_dashboard.html", context)

def register_client(request):
    if request.method == 'POST':
        form = ClientRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  
    else:
        form = ClientRegistrationForm()
    return render(request, 'core/register.html', {'form': form})

def home(request):
    return render(request, 'core/home.html')

@login_required
def request_booking(request, table_id):
    table = get_object_or_404(Table, id=table_id)
    if request.method == 'POST':
        date_val = request.POST.get('date')
        time_val = request.POST.get('time')
        number = request.POST.get('number_of_people', 1)

        if not date_val or not time_val:
            messages.error(request, "Укажите дату и время.")
            return redirect('client_home')

        TableBooking.objects.create(
            table=table,
            client=request.user,
            date=date_val,
            time=time_val,
            number_of_people=number,
            status='pending'
        )
        messages.success(request, f"Заявка на бронирование стола №{table.number} отправлена.")
    return redirect('client_home')

@login_required
def client_home(request):
    if request.user.role != 'client':
        return redirect('login')
    today = date.today()
    now = timezone.now()
    
    # Меню (только доступные блюда)
    menu = MenuItem.objects.filter(is_in_stop_list=False)

    # Столы и их брони
    tables = Table.objects.all()
    booked_table_ids = TableBooking.objects.filter(
        date=today,

        status='booked'
    ).values_list('table_id', flat=True)

    return render(request, 'core/client_home.html', {
        'menu': menu,
        'booked_table_ids': booked_table_ids,
        'tables': tables,
    })


def menu_item_detail(request, item_id):
    item = get_object_or_404(MenuItem, id=item_id)
    return render(request, 'core/menu_item_detail.html', {'item': item})



@login_required
def add_to_order(request, item_id):
    item = get_object_or_404(MenuItem, id=item_id)
    today = timezone.now().date()

    # Получаем бронь клиента на сегодня
    booking = TableBooking.objects.filter(client=request.user, date=today, status='booked').first()
    if not booking:
        messages.error(request, "У вас нет брони на сегодня. Сначала забронируйте стол.")
        return redirect('client_home')

    # Получаем или создаем заказ для клиента и брони
    order, created = Order.objects.get_or_create(
        client=request.user,
        booking=booking,
        defaults={'status': 'pending'}
    )

    # Добавляем пункт меню в заказ (через OrderItem)
    OrderItem.objects.create(
        order=order,
        item=item,
        quantity=1  # можно сделать изменение количества позже
    )

    messages.success(request, f"{item.name} добавлено в заказ.")
    return redirect('client_home')