from django.contrib import admin
from .models import Product, Order

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'customer_name', 'status', 'order_date', 'dispatch_date')
    list_filter = ('status', 'order_date')
    search_fields = ('customer_name', 'customer_email', 'product__name')
    ordering = ('-order_date',)
