from django.db import models
from django.contrib.auth.models import User
from product.models import Product


class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL,
                    blank=True, null=True)
    order_date = models.DateTimeField(auto_now_add=True)
    products = models.ManyToManyField(Product, through='OrderItem')


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE,
                    related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL,
                    related_name='order_items',
                    blank=True, null=True)
    quantity = models.PositiveIntegerField(default=0)
    ordered_price = models.FloatField(default=0)
