from django.contrib import admin

# Register your models here.
from .models import Category
from .models import Product


class CategoryAdmin(admin.ModelAdmin):
    model = Category
    readonly_fields = ['image_preview']
    list_display = ['name_uz', 'name_ru']
    search_fields = ['name_uz', 'name_ru', 'description_uz', 'description_ru']


class ProductAdmin(admin.ModelAdmin):
    model = Product
    readonly_fields = ['image_preview']
    list_display = ['name_uz', 'name_ru', 'price']
    search_fields = ['name_uz', 'name_ru', 'description_uz', 'description_ru']


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
