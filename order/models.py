import uuid

from django.db import models
from telegram.models import User
from product.models import Product

# Create your models here.

# created, pending, accepted, cancelled

STATE_CHOICES = (
    ('created', 'created'),
    ('pending', 'pending'),
    ('accepted', 'accepted'),
    ('cancelled', 'cancelled'),
)

PAYMENT_CHOICES = (
    ('payme', "Payme"),
    ('click', "CLICK"),
    ('cash', "Naqd pul"),
    ('terminal', "Terminal"),
)


class Order(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False,
                          unique=True, primary_key=True)
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        default='created', max_length=100, null=False, blank=False, choices=STATE_CHOICES)
    payment_type = models.CharField(
        max_length=50, null=False, choices=PAYMENT_CHOICES)

    def __str__(self):
        return f'{self.user and self.user.name} at {self.created_at.strftime("%d.%m.%Y %H:%M:%S")}'

    def amount(self):
        price = 0
        for item in self.order_items.all():
            price += item.amount * item.price
        return price


class OrderItem(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False,
                          unique=True, primary_key=True)
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    amount = models.IntegerField(null=False, default=1)
    price = models.IntegerField(null=False, default=0)

    def __str__(self):
        return f"{self.product}"
