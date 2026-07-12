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

    path(
        'add-product/',
        views.add_product,
        name='add_product'
    ),

    path(
        'manage-products/',
        views.manage_products,
        name='manage_products'
    ),

    path(
        'orders/',
        views.orders_page,
        name='orders'
    ),

    path(
        'users/',
        views.users_page,
        name='users'
    ),

    path(
        'pending-requests/',
        views.pending_requests,
        name='pending_requests'
    ),

    path(
        'update-order/<int:order_id>/',
        views.update_order_status,
        name='update_order_status'
    ),

    path(
        'approve-user/<int:user_id>/',
        views.approve_user,
        name='approve_user'
    ),
    path(
        'delete-user/<int:user_id>/',
        views.delete_user,
        name='delete_user'
    ),
    path(
        'edit-product/<int:product_id>/',
        views.edit_product,
        name='edit_product'
    ),

    path(
        'delete-product/<int:product_id>/',
        views.delete_product,
        name='delete_product'
    ),
    path(
        'product/<int:id>/',
        views.product_detail,
        name='product_detail'
    ),
    path(
        'team/',
        views.team_page,
        name='team'
    ),
    path(
        'reject-user/<int:user_id>/',
        views.reject_user,
        name='reject_user'
    ),
    path(
        'sales-report/',
        views.sales_report,
        name='sales_report'
    ), path(
        'download-report/',
        views.download_report,
        name='download_report'
    ),


]
