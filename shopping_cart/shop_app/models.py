from django.db import models

# Create your models here.
class CartItem(models.Model):
    product_name = models.CharField(max_length=200) 
    product_quantity = models.PositiveIntegerField()
    product_price = models.FloatField()