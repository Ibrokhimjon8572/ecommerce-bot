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


class Order(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False,
                          unique=True, primary_key=True)
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        default='created', max_length=100, null=False, blank=False, choices=STATE_CHOICES)

    def __str__(self):
        return self.user.name+" "+str(self.create_at)


class OrderItem(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False,
                          unique=True, primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    amount = models.IntegerField(null=False, default=1)
    price = models.IntegerField(null=False, default=0)

    def __str__(self):
        return self.product.name_uz
