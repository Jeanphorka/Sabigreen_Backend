from django.db import models

class Type(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    weight_grams = models.PositiveIntegerField(null=True, blank=True)  
    price_thb = models.DecimalField(max_digits=10, decimal_places=2)  
    description = models.TextField()
    type = models.ForeignKey(Type, on_delete=models.SET_NULL, null=True, blank=True)
    in_stock = models.PositiveIntegerField(default=0)  
    image = models.ImageField(upload_to='products/' , null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.weight_grams} g)"
