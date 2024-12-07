from django.db import models
from utils.models import BaseFullModel
from utils.importinglibs.data_manipulation_libs import os


class Ingredient(BaseFullModel):
    name = models.CharField(max_length=100, unique=True)
    stock = models.FloatField()  # Stock in grams
    stock_initial = models.FloatField(default=0)  # Initial stock for threshold calculation
    email_sent = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        stock_limit = float(os.environ.get('STOCK_LIMIT'))

        if not self.pk:  # On creation only
            self.stock_initial = self.stock

        # Check if stock is greater than 50% of the stock_initial and set emailSent to False if it is
        if self.stock >= (self.stock_initial * stock_limit):
            self.email_sent = False

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(BaseFullModel):
    name = models.CharField(max_length=100, unique=True)
    ingredients = models.ManyToManyField(Ingredient, through='ProductIngredient')

    def __str__(self):
        return self.name


class ProductIngredient(BaseFullModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.FloatField()  # Quantity of ingredient in grams


class Order(BaseFullModel):
    products = models.ManyToManyField(Product, through='OrderProduct')


class OrderProduct(BaseFullModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
