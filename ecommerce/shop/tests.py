from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from .models import (
    Product,
    Cart,
    Order,
    Coupon,
    UserProfile
)


class EcommerceTest(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            username='ankit',
            password='12345'
        )

        self.product = Product.objects.create(
            name='Python Book',
            description='Programming Book',
            price=500,
            category='Books',
            image='products/test.jpg'
        )

        self.coupon = Coupon.objects.create(
            code='SAVE10',
            discount=10,
            active=True
        )

    # ------------------
    # MODEL TESTS
    # ------------------

    def test_product_creation(self):

        self.assertEqual(
            self.product.name,
            'Python Book'
        )

    def test_coupon_active(self):

        self.assertTrue(
            self.coupon.active
        )

    # ------------------
    # USER TESTS
    # ------------------

    def test_user_creation(self):

        self.assertEqual(
            self.user.username,
            'ankit'
        )

    def test_login(self):

        response = self.client.login(
            username='ankit',
            password='12345'
        )

        self.assertTrue(response)

    # ------------------
    # CART TESTS
    # ------------------

    def test_add_to_cart(self):

        cart = Cart.objects.create(
            user=self.user,
            product=self.product,
            quantity=2
        )

        self.assertEqual(
            cart.quantity,
            2
        )

    # ------------------
    # ORDER TESTS
    # ------------------

    def test_order_creation(self):

        order = Order.objects.create(
            user=self.user,
            product=self.product,
            quantity=1,
            total_price=500
        )

        self.assertEqual(
            order.status,
            'Pending'
        )

    # ------------------
    # PAGE TESTS
    # ------------------

    def test_home_page(self):

        response = self.client.get(
            reverse('home')
        )

        self.assertEqual(
            response.status_code,
            200
        )

    def test_register_page(self):

        response = self.client.get(
            reverse('register')
        )

        self.assertEqual(
            response.status_code,
            200
        )

    def test_login_page(self):

        response = self.client.get(
            reverse('login')
        )

        self.assertEqual(
            response.status_code,
            200
        )

    # ------------------
    # AUTHENTICATED TESTS
    # ------------------

    def test_cart_page(self):

        self.client.login(
            username='ankit',
            password='12345'
        )

        response = self.client.get(
            reverse('cart')
        )

        self.assertEqual(
            response.status_code,
            200
        )

    def test_my_orders_page(self):

        self.client.login(
            username='ankit',
            password='12345'
        )

        response = self.client.get(
            reverse('my_orders')
        )

        self.assertEqual(
            response.status_code,
            200
        )