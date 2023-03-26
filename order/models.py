import uuid

from django.db import models
from telegram.models import User

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
        User, on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        default='created', max_length=100, null=False, blank=False, choices=STATE_CHOICES)
