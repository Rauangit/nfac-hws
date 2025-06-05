from django.urls import path
from .views import register_client
from django.contrib.auth import views as auth_views
from .views import home, register_client, client_home, request_booking
from .views import admin_dashboard
from . import views
from .views import chef_dashboard
from .views import client_dashboard_view, book_table_view, client_bookings_view

urlpatterns = [
    path('register/', register_client, name='register_client'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', home, name='home'),
    path('client/home/', client_home, name='client_home'),
    path('request-booking/<int:table_id>/', request_booking, name='request_booking'),
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    path('menu/<int:item_id>/', views.menu_item_detail, name='menu_item_detail'),
    path('menu/<int:item_id>/add/', views.add_to_order, name='add_to_order'),
    path('chef-dashboard/', chef_dashboard, name='chef_dashboard'),
    path('client/', client_dashboard_view, name='client_dashboard'),
    path('client/book_table/', book_table_view, name='book_table'),
    path('client/bookings/', client_bookings_view, name='client_bookings'),
    path('client/menu-order/<int:booking_id>/', views.menu_order_view, name='menu_order'),  # <--- добавь этот
    path('menu/', views.menu_view, name='menu'),
    path('client/available-tables/', views.available_tables_view, name='available_tables'),
]
