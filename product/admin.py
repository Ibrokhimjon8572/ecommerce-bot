from django.contrib import admin

# Register your models here.
from .models import Category
from .models import Product


class CategoryAdmin(admin.ModelAdmin):
    model = Category
    readonly_fields = ['image_preview']


class ProductAdmin(admin.ModelAdmin):
    model = Product
    readonly_fields = ['image_preview']


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
