from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth import authenticate, login
from .models import UserProfile
from django.shortcuts import render, redirect
from .models import Product
from .models import Coupon
from .forms import ProductForm

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

    products = Product.objects.all()

    categories = Product.objects.values_list(

        'category',

        flat=True

    ).distinct()

    return render(

        request,

        'home.html',

        {

            'products': products,

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

        username = request.POST['username']

        email = request.POST['email']

        password = request.POST['password']

        role = request.POST['role']

        user = User.objects.create_user(

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

def login_page(request):

    if request.method == "POST":

        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            profile = UserProfile.objects.get(user=user)

            # USER LOGIN
            if role == "user":

                login(request, user)
                return redirect('home')

            # ADMIN LOGIN
            elif role == "admin":

                if profile.role == "admin" and profile.approved:

                    login(request, user)
                    return redirect('admin_dashboard')

                else:

                    messages.error(
                        request,
                        "Admin approval pending"
                    )

                    return redirect('login')

        else:

            messages.error(
                request,
                "Invalid username or password"
            )

    return render(request, 'login.html')

# Logout


def logout_page(request):

    logout(
        request
    )

    return redirect(
        'home'
    )


# Admin Dashboard


@login_required
def admin_dashboard(request):

    try:

        profile = UserProfile.objects.get(

            user=request.user

        )

        if profile.role != "admin":

            return redirect(

                'home'

            )

    except UserProfile.DoesNotExist:

        return redirect(

            'home'

        )

    products = Product.objects.all()

    orders = Order.objects.all()

    users = User.objects.all()

    pending = UserProfile.objects.filter(

        approved=False

    )

    return render(

        request,

        'admin_dashboard.html',

        {

            'products': products,

            'orders': orders,

            'users': users,

            'pending': pending

        }

    )


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
def increase_quantity(request, id):

    cart_item = Cart.objects.get(
        id=id
    )

    cart_item.quantity += 1

    cart_item.save()

    return redirect(
        'cart'
    )


@login_required(login_url='/login/')
def decrease_quantity(request, id):

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
def remove_cart(request, id):

    cart_item = Cart.objects.get(
        id=id
    )

    cart_item.delete()

    return redirect(
        'cart'
    )


@login_required(login_url='login')
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

    final_total = total

    coupon = None

    # Session discount

    if request.session.get(

        'discount'

    ):

        discount = request.session.get(

            'discount'

        )

        final_total = total-discount

    if request.method == "POST":

        # Coupon Apply

        if "apply_coupon" in request.POST:

            code = request.POST.get(

                "coupon"

            ).strip()

            try:

                coupon = Coupon.objects.get(

                    code=code,

                    active=True

                )

                discount = (

                    total *
                    coupon.discount

                )/100

                final_total = (

                    total -
                    discount

                )

                request.session[
                    'discount'
                ] = discount

                messages.success(

                    request,

                    "Coupon Applied Successfully"

                )

            except Coupon.DoesNotExist:

                messages.error(

                    request,

                    "Invalid Coupon"

                )

        # Place Order

        elif "place_order" in request.POST:

            payment = request.POST.get(

                'payment'

            )

            for item in cart_items:

                item_total = (

                    item.product.price *
                    item.quantity

                )

                if discount > 0:

                    item_total = (

                        item_total -

                        (

                            item_total *
                            discount /
                            total

                        )

                    )

                Order.objects.create(

                    user=request.user,

                    product=item.product,

                    quantity=item.quantity,

                    total_price=item_total,

                    payment_method=payment,

                    status='Pending'

                )

            cart_items.delete()

            request.session.pop(

                'discount',

                None

            )

            return redirect(

                'order_success'

            )

    # QR Code Generate

    upi_id = "ankitprashar88@oksbi"

    upi_link = f"upi://pay?pa={upi_id}&pn=StudentEssentials&am={final_total}&cu=INR"

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

            'final_total': final_total,

            'coupon': coupon,

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
    ).order_by(
        '-created_at'
    )

    return render(

        request,

        'my_orders.html',

        {
            'orders': orders
        }

    )


@login_required
def add_product(request):

    if request.method == "POST":

        form = ProductForm(

            request.POST,
            request.FILES

        )

        if form.is_valid():

            form.save()

            return redirect(
                'manage_products'
            )

    else:

        form = ProductForm()

    return render(

        request,

        'add_product.html',

        {

            'form': form

        }

    )


@login_required
def manage_products(request):

    products = Product.objects.all()

    return render(

        request,

        'manage_products.html',

        {

            'products': products

        }

    )


@login_required
def orders_page(request):

    orders = Order.objects.all()

    return render(

        request,

        'orders.html',

        {

            'orders': orders

        }

    )


@login_required
def users_page(request):

    users = UserProfile.objects.all()

    return render(

        request,

        'users.html',

        {

            'users': users

        }

    )


@login_required
def pending_requests(request):

    pending = UserProfile.objects.filter(
        approved=False
    )

    return render(

        request,

        'pending_requests.html',

        {

            'pending': pending

        }

    )


@login_required
def update_order_status(

    request,
    order_id

):

    order = Order.objects.get(

        id=order_id

    )

    if request.method == "POST":

        order.status = request.POST.get(

            'status'

        )

        order.save()

    return redirect(

        'orders'

    )


@login_required
def approve_user(
    request,
    user_id
):
    profile = UserProfile.objects.get(
        id=user_id
    )
    profile.approved = True
    profile.save()
    profile.user.is_staff = True
    profile.user.save()
    return redirect(
        'pending_requests'
    )


@login_required
def reject_user(
    request,
    user_id
):
    profile = UserProfile.objects.get(
        id=user_id
    )
    profile.delete()
    return redirect(
        'pending_requests'
    )


@login_required
def delete_user(request, user_id):

    profile = UserProfile.objects.get(

        id=user_id

    )

    profile.user.delete()

    return redirect(

        'users'
    )


@login_required
def edit_product(
    request,
    product_id
):

    product = Product.objects.get(
        id=product_id
    )

    if request.method == "POST":

        product.name = request.POST['name']

        product.price = request.POST['price']

        product.category = request.POST['category']

        if 'image' in request.FILES:

            product.image = request.FILES['image']

        product.save()

        return redirect(
            'manage_products'
        )

    return render(

        request,

        'edit_product.html',

        {

            'product': product

        }

    )


@login_required
def delete_product(
    request,
    product_id
):

    product = Product.objects.get(

        id=product_id

    )

    product.delete()

    return redirect(

        'manage_products'
    )


@login_required
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


def team_page(request):

    return render(

        request,

        'team.html'

    )


def reject_user(request, user_id):

    profile = get_object_or_404(
        UserProfile,
        id=user_id
    )

    profile.user.delete()

    return redirect('pending_requests')


from django.db.models import Sum
from .models import Order

def sales_report(request):

    orders = Order.objects.all()

    total_orders = orders.count()

    total_revenue = orders.aggregate(
        Sum('total_price')
    )['total_price__sum'] or 0

    return render(
        request,
        'sales_report.html',
        {
            'orders': orders,
            'total_orders': total_orders,
            'total_revenue': total_revenue
        }
    )

import csv

from django.http import HttpResponse

from .models import Order


def download_report(request):

    response = HttpResponse(
        content_type='text/csv'
    )

    response[
        'Content-Disposition'
    ] = 'attachment; filename="sales_report.csv"'


    writer = csv.writer(response)

    writer.writerow([
        'Order ID',
        'Customer',
        'Amount',
        'Status'
    ])


    orders = Order.objects.all()

    for order in orders:

        writer.writerow([
            order.id,
            order.user.username,
            order.total_price,
            order.status
        ])

    return response
