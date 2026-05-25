from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.IntegerField()
    image = models.ImageField(upload_to='products/')
    category = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
from django.contrib.auth.models import User

class Cart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )
    quantity = models.IntegerField(
        default=1
    )
    def __str__(self):
        return self.user.username
    
class Order(models.Model):

    STATUS_CHOICES = [

        ('Pending','Pending'),
        ('Processing','Processing'),
        ('Shipped','Shipped'),
        ('Delivered','Delivered')

    ]


    PAYMENT_CHOICES = [

        ('COD','Cash On Delivery'),

        ('QR','UPI QR'),

        ('CARD','Card Payment')

    ]


    user = models.ForeignKey(

        User,

        on_delete=models.CASCADE

    )

    product = models.ForeignKey(

        Product,

        on_delete=models.CASCADE

    )

    quantity = models.IntegerField()


    total_price = models.DecimalField(

        max_digits=10,

        decimal_places=2

    )


    payment_method = models.CharField(

        max_length=20,

        choices=PAYMENT_CHOICES,

        default='COD'

    )


    status = models.CharField(

        max_length=20,

        choices=STATUS_CHOICES,

        default='Pending'

    )


    created_at = models.DateTimeField(

        auto_now_add=True

    )


    def __str__(self):

        return self.user.username
    
from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):

    user=models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    role=models.CharField(
        max_length=20,
        choices=[
            ('user','User'),
            ('admin','Admin')
        ]
    )

    approved=models.BooleanField(
        default=False
    )

    def __str__(self):

        return self.user.username
    
class Coupon(models.Model):

    code=models.CharField(
        max_length=50,
        unique=True
    )

    discount=models.IntegerField()

    active=models.BooleanField(
        default=True
    )

    def __str__(self):

        return self.code