from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpRequest, HttpResponse
from .models import Product, Category


def _get_cart(session) -> dict:
    cart = session.get('cart', {})
    if not isinstance(cart, dict):
        cart = {}
    return cart


def home(request: HttpRequest) -> HttpResponse:
    latest_products = Product.objects.order_by('-created_at')[:8]
    categories = Category.objects.all()
    return render(request, 'home.html', {
        'latest_products': latest_products,
        'categories': categories,
    })


def product_list(request: HttpRequest) -> HttpResponse:
    category_slug = request.GET.get('category')
    products = Product.objects.all()
    active_category = None
    if category_slug:
        active_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=active_category)
    categories = Category.objects.all()
    return render(request, 'product_list.html', {
        'products': products,
        'categories': categories,
        'active_category': active_category,
    })


def product_detail(request: HttpRequest, slug: str) -> HttpResponse:
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'product_detail.html', {'product': product})


def cart_detail(request: HttpRequest) -> HttpResponse:
    session = request.session
    cart = _get_cart(session)
    product_ids = list(cart.keys())
    products = Product.objects.filter(id__in=product_ids)
    items = []
    subtotal_cents = 0
    for product in products:
        quantity = int(cart.get(str(product.id), 0))
        line_total = product.price_cents * quantity
        subtotal_cents += line_total
        items.append({
            'product': product,
            'quantity': quantity,
            'line_total_cents': line_total,
            'line_total_display': f"${line_total / 100:.2f}",
        })
    return render(request, 'cart.html', {
        'items': items,
        'subtotal_cents': subtotal_cents,
        'subtotal_display': f"${subtotal_cents / 100:.2f}",
    })


def cart_add(request: HttpRequest, product_id: int) -> HttpResponse:
    session = request.session
    cart = _get_cart(session)
    key = str(product_id)
    cart[key] = int(cart.get(key, 0)) + 1
    session['cart'] = cart
    session.modified = True
    return redirect('cart_detail')


def cart_remove(request: HttpRequest, product_id: int) -> HttpResponse:
    session = request.session
    cart = _get_cart(session)
    key = str(product_id)
    if key in cart:
        del cart[key]
        session['cart'] = cart
        session.modified = True
    return redirect('cart_detail')


def checkout(request: HttpRequest) -> HttpResponse:
    session = request.session
    cart = _get_cart(session)
    if not cart:
        return redirect('product_list')
    return render(request, 'checkout.html')

# Create your views here.
