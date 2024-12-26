from django.shortcuts import redirect, get_object_or_404, render
from .models import Product, Order

# Display the list of products
def product_list(request):
    products = Product.objects.all()[:10]  # Get the first 10 products
    return render(request, 'store/product_list.html', {'products': products})

# Handle order placement
def place_order(request, product_id):
    if request.method == "POST":
        product = get_object_or_404(Product, id=product_id)
        customer_name = request.POST.get('customer_name', 'Anonymous')  # Placeholder, you can extend this
        customer_email = request.POST.get('customer_email', 'anonymous@example.com')  # Placeholder
        order = Order.objects.create(
            product=product,
            customer_name=customer_name,
            customer_email=customer_email
        )
        return redirect('order_success')  # Redirect after successful order
    return redirect('product_list')  # Redirect if accessed via GET

# Display order success page
def order_success(request):
    return render(request, 'store/order_success.html')
