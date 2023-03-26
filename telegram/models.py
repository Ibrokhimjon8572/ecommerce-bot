import uuid

from django.db import models
from product.models import Category, Product

LANGUAGE_CHOICES = (
    ('uz', "O'zbek"),
    ('ru', "Русский"),
)

STATE_CHOICES = (
    ('start', 'Start'),
    ('select_language', 'Selecting language'),
    ('ask_phone', 'Waiting for phone number'),
    ('main_menu', 'Main menu'),
    ('categories', 'Browsing categories'),
    ('products', 'Browsing products'),
    ('amount', 'Choosing amount'),
    ('basket', 'Basket'),
    ('order', 'Ordering'),
)


# Create your models here.
class User(models.Model):
    id = models.UUIDField(default=uuid.uuid4,
                          primary_key=True, unique=True, editable=False)
    language = models.CharField(
        max_length=2, null=False, default='uz', choices=LANGUAGE_CHOICES)
    user_id = models.IntegerField(null=False, unique=True)
    username = models.CharField(max_length=50, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=False)
    name = models.CharField(max_length=30, null=True, blank=False)

    def __str__(self):
        return self.name


class UserSession(models.Model):
    user = models.OneToOneField(
        User, related_name='session', on_delete=models.CASCADE)
    state = models.CharField(max_length=50, null=False, choices=STATE_CHOICES)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    amount = models.IntegerField(default=0)
