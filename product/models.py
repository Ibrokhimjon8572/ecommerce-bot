import uuid

from django.db import models
from django.utils.html import mark_safe
# Create your models here.


class Category(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    name_uz = models.CharField(null=True, max_length=50)
    name_ru = models.CharField(null=True, max_length=50)
    description_uz = models.TextField(
        null=True, blank=True, max_length=300, verbose_name="Description in Uzbek")
    description_ru = models.TextField(
        null=True, blank=True, max_length=300, verbose_name="Description in Russian")
    image = models.ImageField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Categories"

    def image_preview(self):
        return mark_safe(f'<img src = "{self.image.url}" style="width: 100%" />')

    def __str__(self):
        return self.name_uz


class Product(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    name_uz = models.CharField(null=True, max_length=50)
    name_ru = models.CharField(null=True, max_length=50)
    description_uz = models.TextField(
        null=True, blank=True, max_length=300, verbose_name="Description in Uzbek")
    description_ru = models.TextField(
        null=True, blank=True, max_length=300, verbose_name="Description in Russian")
    price = models.IntegerField(null=False, default=0)
    category = models.ForeignKey(
        Category, related_name='products', on_delete=models.CASCADE)
    image = models.ImageField(blank=True, null=True)

    def image_preview(self):
        return mark_safe(f'<img src = "{self.image.url}" style="width: 100%" />')

    def __str__(self):
        return self.name_uz
