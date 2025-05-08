from django.db import models
from products.models import Product
from decimal import Decimal

class Order(models.Model):
    order_number = models.CharField(max_length=30, unique=True, blank=True, null=True)
    full_name = models.CharField(max_length=255)
    address = models.TextField()
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)

    DELIVERY_CHOICES = [
    ('รับหน้าร้าน', 'รับหน้าร้าน'),
    ('จัดส่งทางไปรษณีย์', 'จัดส่งทางไปรษณีย์'),
]
    delivery_method = models.CharField(max_length=20, choices=DELIVERY_CHOICES)
    shipping_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def total_price(self):
        item_total = sum(item.total_price for item in self.items.all())
        return item_total + Decimal(str(self.shipping_fee))

    def __str__(self):
        return f"Order #{self.id} - {self.full_name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_price(self):
        return self.product.price_thb * self.quantity

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
