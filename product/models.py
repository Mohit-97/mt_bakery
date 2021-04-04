from django.db import models

from django.contrib.auth.models import User


class Product(models.Model):
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=255, null=True, blank=True)
    cost_price = models.FloatField(default=0)
    selling_price = models.FloatField(default=0)
    available_quantity = models.PositiveIntegerField(default=0)
    ingredients = models.ManyToManyField('Ingredients',
        through='ProductIngredient', related_name='product_ingredients')
    is_active = models.BooleanField(default=True)
    added_on = models.DateTimeField(auto_now_add=True)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL,
        related_name='product_added_by', null=True, blank=True)
    updated_on = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL,
                    null=True, blank=True, related_name='product_updated_by')

    def __str__(self):
        return "{} = ${}".format(self.name, self.selling_price)


class InventoryTransactions(models.Model):
    ADD, REMOVE = 1, 2,
    ACTION_CHOICES = (
        (ADD, 'add'),
        (REMOVE, 'remove'),
    )
    action = models.PositiveIntegerField(choices=ACTION_CHOICES)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_on = models.DateTimeField(auto_now_add=True)
    quantity = models.PositiveIntegerField(default=0)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL,
                    null=True, blank=True,)


class Ingredients(models.Model):
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return "{}".format(self.name)


class ProductIngredient(models.Model):
    product = models.ForeignKey(Product, related_name='products',
                on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredients, related_name='products',
                on_delete=models.SET_NULL, blank=True, null=True)
    quantity_percent = models.FloatField(default=0)
