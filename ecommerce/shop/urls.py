from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name='home'),

    path(
        'login/',
        views.login_page,
        name='login'
    ),

    path(
        'register/',
        views.register_page,
        name='register'
    ),

    path(
        'logout/',
        views.logout_page,
        name='logout'
    ),

    path(
        'admin-dashboard/',
        views.admin_dashboard,
        name='admin_dashboard'
    ),

    path(
        'category/<str:category>/',
        views.category_products,
        name='category_products'
    ),
    path(
        'product/<int:id>/',
        views.product_detail,
        name='product_detail'
    ),
    path(
        'add-to-cart/<int:id>/',
        views.add_to_cart,
        name='add_to_cart'
    ),
    path(
        'cart/',
        views.cart_page,
        name='cart'
    ),
    path(
        'increase/<int:id>/',
        views.increase_quantity,
        name='increase_quantity'
    ),

    path(
        'decrease/<int:id>/',
        views.decrease_quantity,
        name='decrease_quantity'
    ),

    path(
        'remove/<int:id>/',
        views.remove_cart,
        name='remove_cart'
    ),
    path(
        'checkout/',
        views.checkout,
        name='checkout'
    ),

    path(
        'order-success/',
        views.order_success,
        name='order_success'
    ),
    path(
        'my-orders/',
        views.my_orders,
        name='my_orders'
    ),
]