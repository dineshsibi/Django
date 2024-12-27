from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('order/<int:product_id>/', views.place_order, name='order'),
    path('order-success/', views.order_success, name='order_success'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('product/<int:product_id>/order/', views.place_order, name='place_order'),  # Define the URL for place_order
    path('customer-dashboard/', views.customer_dashboard, name='customer_dashboard'),
   
]
