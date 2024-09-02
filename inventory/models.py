from django.db import models
from django.core.validators import MinValueValidator

class Product(models.Model):
    name = models.CharField(max_length=150)
    actual_price = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    offer_price = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=0, validators=[MinValueValidator(0)])

    def __str__(self):
        return f"{self.name} - {self.quantity} qty"