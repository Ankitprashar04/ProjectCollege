from django.shortcuts import render, redirect
from .models import Product

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Product, Cart

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


# Home Page
def home(request):

    categories = Product.objects.values_list(
        'category',
        flat=True
    ).distinct()

    return render(
        request,
        'home.html',
        {
            'categories': categories
        }
    )


# Category Products
def category_products(request, category):

    products = Product.objects.filter(
        category=category
    )

    return render(
        request,
        'category.html',
        {
            'products': products,
            'category': category
        }
    )


# Register
def register_page(request):

    if request.method == "POST":

        username = request.POST.get(
            'username'
        )

        email = request.POST.get(
            'email'
        )

        password = request.POST.get(
            'password'
        )

        confirm_password = request.POST.get(
            'confirm_password'
        )


        if password != confirm_password:

            messages.error(
                request,
                "Passwords do not match"
            )

            return redirect(
                'register'
            )


        if User.objects.filter(
            username=username
        ).exists():

            messages.error(
                request,
                "Username already exists"
            )

            return redirect(
                'register'
            )


        if User.objects.filter(
            email=email
        ).exists():

            messages.error(
                request,
                "Email already exists"
            )

            return redirect(
                'register'
            )


        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )


        messages.success(
            request,
            "Registration successful"
        )

        return redirect(
            'login'
        )

    return render(
        request,
        'register.html'
    )


# Login
def login_page(request):

    if request.method == "POST":

        username = request.POST.get(
            'username'
        )

        password = request.POST.get(
            'password'
        )


        user = authenticate(
            request,
            username=username,
            password=password
        )


        if user is not None:

            login(
                request,
                user
            )

            return redirect(
                'home'
            )

        else:

            messages.error(
                request,
                "Invalid Username or Password"
            )

    return render(
        request,
        'login.html'
    )


# Logout
def logout_page(request):

    logout(
        request
    )

    return redirect(
        'home'
    )


# Admin Dashboard
@login_required(
    login_url='/login/'
)
def admin_dashboard(request):

    if not request.user.is_staff:

        return HttpResponse(
            "Access Denied"
        )


    products = Product.objects.all()

    return render(
        request,
        'admin_dashboard.html',
        {
            'products': products
        }
    )

def product_detail(request, id):

    product = Product.objects.get(
        id=id
    )

    return render(
        request,
        'product_detail.html',
        {
            'product': product
        }
    )

from django.contrib.auth.decorators import login_required


@login_required(login_url='/login/')
def add_to_cart(request, id):

    product = Product.objects.get(
        id=id
    )

    cart_item, created = Cart.objects.get_or_create(

        user=request.user,
        product=product
    )

    if not created:

        cart_item.quantity += 1

        cart_item.save()

    return redirect(
        'cart'
    )

@login_required(login_url='/login/')
def cart_page(request):

    cart_items = Cart.objects.filter(
        user=request.user
    )

    total = 0

    for item in cart_items:

        total += (
            item.product.price *
            item.quantity
        )

    return render(
        request,
        'cart.html',
        {
            'cart_items': cart_items,
            'total': total
        }
    )

@login_required(login_url='/login/')
def increase_quantity(request,id):

    cart_item = Cart.objects.get(
        id=id
    )

    cart_item.quantity += 1

    cart_item.save()

    return redirect(
        'cart'
    )



@login_required(login_url='/login/')
def decrease_quantity(request,id):

    cart_item = Cart.objects.get(
        id=id
    )

    if cart_item.quantity > 1:

        cart_item.quantity -= 1

        cart_item.save()

    return redirect(
        'cart'
    )



@login_required(login_url='/login/')
def remove_cart(request,id):

    cart_item = Cart.objects.get(
        id=id
    )

    cart_item.delete()

    return redirect(
        'cart'
    )