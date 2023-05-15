from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse

# Register your models here.
from .models import Category
from .models import Product


class CategoryInline(admin.TabularInline):
    model = Category
    fields = ['name_uz', "description_uz", "admin_link"]
    show_change_link = False
    readonly_fields = ["admin_link"]

    def admin_link(self, instance):
        url = reverse('admin:%s_%s_change' % (instance._meta.app_label,
                                              instance._meta.model_name),
                      args=(instance.id,))
        return format_html('<a href="{}">Edit</a>', url)

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class ProductInline(admin.TabularInline):
    model = Product
    fields = ['name_uz', "description_uz", "price", "admin_link"]
    show_change_link = False
    readonly_fields = ["admin_link"]

    def admin_link(self, instance):
        url = reverse('admin:%s_%s_change' % (instance._meta.app_label,
                                              instance._meta.model_name),
                      args=(instance.id,))
        return format_html('<a href="{}">Edit</a>', url)

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class CategoryAdmin(admin.ModelAdmin):
    model = Category
    readonly_fields = ['image_preview']
    list_display = ['__str__', 'name_uz', 'name_ru', 'is_product_category']
    search_fields = ['name_uz', 'name_ru', 'description_uz', 'description_ru']
    list_filter = ['parent']
    inlines = [CategoryInline, ProductInline]

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
