from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Order
from django.utils.timezone import now
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required

# Product listing view
def product_list(request):
    products = Product.objects.all()
    return render(request, 'store/product_list.html', {'products': products})

# Place an order
def place_order(request, product_id):
    if request.method == "POST":
        product = get_object_or_404(Product, id=product_id)
        order = Order.objects.create(
            product=product,
            customer=request.user,
            customer_name=request.user.username,
            customer_email=request.user.email
        )
        return redirect('order_success')
    return redirect('product_list')

# Order success page
def order_success(request):
    return render(request, 'store/order_success.html')

# Admin dashboard to manage orders
def admin_dashboard(request):
    if request.method == "POST":
        order_id = request.POST.get('order_id')
        dispatch_date = request.POST.get('dispatch_date')
        if order_id and dispatch_date:
            order = Order.objects.get(id=order_id)
            order.status = 'Dispatched'
            order.dispatch_date = dispatch_date
            order.save()
    orders = Order.objects.all()
    return render(request, 'store/admin_dashboard.html', {'orders': orders})

# Customer registration view
def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        return redirect('login')
    return render(request, 'store/register.html')

# Customer login view
def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            auth_login(request, user)
            return redirect('customer_dashboard')
        else:
            return render(request, 'store/login.html', {'error': 'Invalid credentials'})
    return render(request, 'store/login.html')

# Customer dashboard view
@login_required
def customer_dashboard(request):
    orders = Order.objects.filter(customer=request.user)
    products = Product.objects.all()
    return render(request, 'store/customer_dashboard.html', {'orders': orders, 'products': products})
