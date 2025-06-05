from django.contrib import admin
from .models import User, TableBooking, MenuItem, Order, Table
from django import forms


class TableBookingForm(forms.ModelForm):
    class Meta:
        model = TableBooking
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['client'].queryset = User.objects.filter(role='client')


@admin.register(TableBooking)
class TableBookingAdmin(admin.ModelAdmin):
    form = TableBookingForm
    list_display = ('client', 'date', 'time', 'number_of_people', 'status')
    list_filter = ('status', 'date')
    search_fields = ('client__username',)


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ('number', 'capacity', 'is_available', 'toggle_status_button')
    list_editable = ('is_available',)
    actions = ['mark_as_available', 'mark_as_unavailable']

    def mark_as_available(self, request, queryset):
        updated = queryset.update(is_available=True)
        self.message_user(request, f"{updated} стол(ов) отмечено как свободные.")
    mark_as_available.short_description = "Отметить как свободные"

    def mark_as_unavailable(self, request, queryset):
        updated = queryset.update(is_available=False)
        self.message_user(request, f"{updated} стол(ов) отмечено как занятые.")
    mark_as_unavailable.short_description = "Отметить как занятые"

    def toggle_status_button(self, obj):
        return "✔️" if obj.is_available else "❌"
    toggle_status_button.short_description = "Доступен?"


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')
    search_fields = ('username', 'email')


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'preparation_time', 'is_in_stop_list')
    list_filter = ('is_in_stop_list',)
    search_fields = ('name',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'booking', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('client__username',)
