from django.contrib import admin

# Register your models here.
from .models import Category
from .models import Product


class CategoryAdmin(admin.ModelAdmin):
    model = Category
    readonly_fields = ['image_preview']
    list_display = ['__str__', 'name_uz', 'name_ru', 'is_product_category']
    search_fields = ['name_uz', 'name_ru', 'description_uz', 'description_ru']
    list_filter = ['parent']

    def render_change_form(self, request, context, *args, **kwargs):
        context['adminform'].form.fields['parent'].queryset = Category.objects.filter(
            is_product_category=False)
        return super(CategoryAdmin, self).render_change_form(request, context, *args, **kwargs)


class ProductAdmin(admin.ModelAdmin):
    model = Product
    readonly_fields = ['image_preview']
    list_display = ['__str__', 'name_uz', 'name_ru', 'price']
    search_fields = ['name_uz', 'name_ru', 'description_uz', 'description_ru']

    def render_change_form(self, request, context, *args, **kwargs):
        context['adminform'].form.fields['category'].queryset = Category.objects.filter(
            is_product_category=True)
        return super(ProductAdmin, self).render_change_form(request, context, *args, **kwargs)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
