# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Order
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required


# Product listing view
def product_list(request):
    products = Product.objects.all()
    return render(request, 'store/product_list.html', {'products': products})


# Add to Cart functionality
@login_required
def add_to_cart(request, product_id):
    cart = request.session.get('cart', [])
    cart.append(product_id)
    request.session['cart'] = cart
    return redirect('customer_dashboard')


# Customer dashboard view
@login_required
def customer_dashboard(request):
    products = Product.objects.all()
    cart = request.session.get('cart', [])
    cart_products = Product.objects.filter(id__in=cart)
    orders = Order.objects.filter(customer=request.user)  # Show orders placed by the logged-in customer
    return render(request, 'store/customer_dashboard.html', {
        'products': products,
        'cart_products': cart_products,
        'orders': orders
    })


# Checkout functionality
@login_required
def checkout(request):
    cart = request.session.get('cart', [])
    if not cart:
        return redirect('customer_dashboard')  # Redirect if cart is empty

    cart_products = Product.objects.filter(id__in=cart)

    if request.method == "POST":
        address = request.POST.get('address')
        customer_name = request.user.username
        customer_email = request.user.email

        # Create an order for each product in the cart
        for product in cart_products:
            Order.objects.create(
                product=product,
                customer=request.user,  # Associate the order with the logged-in user
                customer_name=customer_name,
                customer_email=customer_email,
                address=address
            )

        # Clear the cart after placing the order
        request.session['cart'] = []
        return redirect('order_success')

    return render(request, 'store/checkout.html', {'cart_products': cart_products})


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

def place_order(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    customer_name = request.user.username
    customer_email = request.user.email
    address = request.POST.get('address')

    Order.objects.create(
        product=product,
        customer_name=customer_name,
        customer_email=customer_email,
        address=address
    )
    return redirect('customer_dashboard')
