from django.contrib import admin

# Register your models here.
from .models import Category


class CategoryAdmin(admin.ModelAdmin):
    model = Category
    readonly_fields = ['image_preview']


admin.site.register(Category, CategoryAdmin)
