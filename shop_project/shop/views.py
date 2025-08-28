from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .models import Product
from .forms import ReturnRequestForm
from django.contrib.auth.decorators import login_required


# Homepage
def home(request):
    return render(request, 'shop/home.html')


# Product listing
def products(request):
    items = Product.objects.all()
    return render(request, "shop/products.html", {"products": items})


# About page
def about(request):
    return render(request, "shop/about.html")


# Contact form
@csrf_exempt   # (Later, switch to Django forms for CSRF safety)
def contact(request):
    success = False
    if request.method == "POST":
        # Example: process contact form (name, email, message)
        success = True
    return render(request, "shop/contact.html", {"success": success})


# Shopping cart (session-based)
def cart(request):
    cart_items = request.session.get("cart", [])
    products = Product.objects.filter(id__in=cart_items)
    return render(request, "shop/cart.html", {"cart": products})


# Add product to cart
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get("cart", [])
    if product.id not in cart:
        cart.append(product.id)
        request.session["cart"] = cart
    return redirect("cart")


# Remove product from cart
def remove_from_cart(request, product_id):
    cart = request.session.get("cart", [])
    if product_id in cart:
        cart.remove(product_id)
        request.session["cart"] = cart
    return redirect("cart")


# My orders (history)
@login_required
def my_orders(request):
    orders = request.user.orders.all()  # fetch orders of the logged-in user
    return render(request, "shop/my_orders.html", {"orders": orders})


# Return & refund page (real implementation)
@login_required
@csrf_exempt
def return_refund(request):
    success = False
    if request.method == "POST":
        form = ReturnRequestForm(request.POST, user=request.user)
        if form.is_valid():
            return_request = form.save(commit=False)
            return_request.status = "PENDING"
            return_request.save()
            success = True
    else:
        form = ReturnRequestForm(user=request.user)

    return render(request, "shop/return_refund.html", {"form": form, "success": success})
