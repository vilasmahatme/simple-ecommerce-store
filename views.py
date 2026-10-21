from decimal import Decimal
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from .models import Product, Order, OrderItem

def product_list(request):
    products = Product.objects.all().order_by("name")
    return render(request, "shop/product_list.html", {"products": products})

def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, "shop/product_detail.html", {"product": product})

def _cart_items(request):
    cart = request.session.get("cart", {})
    items, total, count = [], Decimal("0.00"), 0
    for product_id, quantity in cart.items():
        try:
            product = Product.objects.get(pk=int(product_id))
            quantity = max(1, int(quantity))
        except (Product.DoesNotExist, ValueError, TypeError):
            continue
        line_total = product.price * quantity
        items.append({"product": product, "quantity": quantity, "line_total": line_total})
        total += line_total
        count += quantity
    return items, total, count

def cart_view(request):
    items, total, count = _cart_items(request)
    return render(request, "shop/cart.html", {"items": items, "total": total, "cart_count": count})

@require_POST
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if product.stock < 1:
        messages.error(request, "This product is out of stock.")
        return redirect("product_detail", product_id=product.pk)
    cart = request.session.get("cart", {})
    key = str(product.pk)
    cart[key] = min(int(cart.get(key, 0)) + 1, product.stock)
    request.session["cart"] = cart
    messages.success(request, f"{product.name} added to your cart.")
    return redirect(request.POST.get("next") or "cart")

@require_POST
def update_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    try:
        quantity = int(request.POST.get("quantity", "1"))
    except ValueError:
        quantity = 1
    cart = request.session.get("cart", {})
    if quantity <= 0:
        cart.pop(str(product_id), None)
    else:
        cart[str(product_id)] = min(quantity, product.stock)
    request.session["cart"] = cart
    return redirect("cart")

@require_POST
def remove_from_cart(request, product_id):
    cart = request.session.get("cart", {})
    cart.pop(str(product_id), None)
    request.session["cart"] = cart
    messages.info(request, "Product removed from cart.")
    return redirect("cart")

@login_required
def checkout(request):
    items, total, count = _cart_items(request)
    if not items:
        messages.info(request, "Your cart is empty.")
        return redirect("product_list")
    if request.method == "POST":
        full_name = request.POST.get("full_name", "").strip()
        address = request.POST.get("address", "").strip()
        phone = request.POST.get("phone", "").strip()
        if not full_name or not address or not phone:
            messages.error(request, "Please complete all checkout fields.")
            return render(request, "shop/checkout.html", {"items": items, "total": total})
        for item in items:
            if item["quantity"] > item["product"].stock:
                messages.error(request, f"Not enough stock for {item['product'].name}.")
                return redirect("cart")
        order = Order.objects.create(
            user=request.user, full_name=full_name, address=address,
            phone=phone, total=total
        )
        for item in items:
            product = item["product"]
            quantity = item["quantity"]
            OrderItem.objects.create(
                order=order, product=product, product_name=product.name,
                price=product.price, quantity=quantity
            )
            product.stock -= quantity
            product.save(update_fields=["stock"])
        request.session["cart"] = {}
        messages.success(request, f"Order #{order.pk} placed successfully!")
        return redirect("order_history")
    return render(request, "shop/checkout.html", {"items": items, "total": total})

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Your account has been created.")
            return redirect("product_list")
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {"form": form})

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).prefetch_related("items").order_by("-created_at")
    return render(request, "shop/order_history.html", {"orders": orders})
