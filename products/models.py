from django.db import models

class TeaType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    weight_grams = models.PositiveIntegerField()  # น้ำหนักหน่วยกรัม เช่น 500
    price_thb = models.DecimalField(max_digits=10, decimal_places=2)  # เช่น 750.00
    description = models.TextField()
    tea_type = models.ForeignKey(TeaType, on_delete=models.SET_NULL, null=True, blank=True)
    in_stock = models.PositiveIntegerField(default=0)  # จำนวนสินค้าคงเหลือ
    image = models.ImageField(upload_to='products/' , null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.weight_grams} g)"
