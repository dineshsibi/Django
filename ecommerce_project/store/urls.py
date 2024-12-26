from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('order/<int:product_id>/', views.place_order, name='order'),
    path('order-success/', views.order_success, name='order_success'),
]

