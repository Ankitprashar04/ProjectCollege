from django.contrib import admin
from .models import Product, UserProfile

admin.site.register(Product)
admin.site.register(
    UserProfile
)

from .models import Coupon

admin.site.register(
    Coupon
)