from django.shortcuts import render, redirect
from .models import Product
from .models import Coupon

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Product, Cart, Order
import razorpay
from django.conf import settings

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import qrcode
from io import BytesIO
from base64 import b64encode


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
from .models import UserProfile


def register_page(request):

    if request.method=="POST":

        username=request.POST['username']

        email=request.POST['email']

        password=request.POST['password']

        role=request.POST['role']


        user=User.objects.create_user(

            username=username,
            email=email,
            password=password
        )


        UserProfile.objects.create(

            user=user,

            role=role,

            approved=False
        )


        messages.success(

            request,

            "Registration submitted. Wait for approval."
        )

        return redirect(
            'login'
        )


    return render(
        request,
        'register.html'
    )

# Login
from django.contrib.auth import authenticate,login
from django.contrib import messages
from django.shortcuts import render,redirect


def login_page(request):

    if request.method=="POST":

        username=request.POST['username']

        password=request.POST['password']

        role=request.POST['role']


        user=authenticate(

            username=username,
            password=password

        )


        if user is not None:

            from .models import UserProfile

            profile=UserProfile.objects.get(
                user=user
            )


            # Approval check

            if not profile.approved:

                messages.error(

                    request,

                    "Account pending approval"

                )

                return redirect(
                    'login'
                )


            # Admin selected

            if role=="admin":

                if profile.role=="admin":

                    login(
                        request,
                        user
                    )

                    return redirect(
                        'admin_dashboard'
                    )

                else:

                    messages.error(

                        request,

                        "Access denied: You are not admin"

                    )

                    return redirect(
                        'login'
                    )


            # User selected

            elif role=="user":

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
from django.contrib.auth.models import User
from .models import Product
from .models import UserProfile


def admin_dashboard(request):

    products=Product.objects.all()

    users=User.objects.all()

    pending=UserProfile.objects.filter(
        approved=False
    )

    return render(

        request,

        'admin_dashboard.html',

        {

            'products':products,

            'users':users,

            'pending':pending

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


@login_required(login_url='/login/')
def checkout(request):

    cart_items = Cart.objects.filter(
        user=request.user
    )

    total = sum(

        item.product.price *
        item.quantity

        for item in cart_items

    )

    discount = 0
    coupon = None


    if request.method == "POST":

        coupon_code = request.POST.get(
            'coupon'
        )

        if coupon_code:

            try:

                coupon = Coupon.objects.get(

                    code=coupon_code,
                    active=True

                )

                discount = (

                    total *
                    coupon.discount

                ) / 100


                messages.success(

                    request,

                    "Coupon Applied Successfully"

                )

            except:

                messages.error(

                    request,

                    "Invalid Coupon"

                )


    final_total = total - discount


    upi_id = "ankitprashar88@oksbi"


    upi_link = (

        f"upi://pay?"

        f"pa={upi_id}"

        f"&pn=StudentEssentials"

        f"&am={final_total}"

        f"&cu=INR"

    )


    qr = qrcode.make(
        upi_link
    )

    buffer = BytesIO()

    qr.save(
        buffer,
        format="PNG"
    )


    qr_code = b64encode(

        buffer.getvalue()

    ).decode()



    return render(

        request,

        'checkout.html',

        {

            'cart_items': cart_items,

            'total': total,

            'discount': discount,

            'coupon': coupon,

            'final_total': final_total,

            'qr_code': qr_code

        }

    )

def order_success(request):

    return render(
        request,
        'order_success.html'
    )

@login_required(login_url='/login/')
def my_orders(request):

    orders = Order.objects.filter(
        user=request.user
    )

    return render(
        request,
        'my_orders.html',
        {
            'orders': orders
        }
    )