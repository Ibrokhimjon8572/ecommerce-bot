from django.contrib import admin
from .models import Order, OrderItem

# Register your models here.


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ['product', 'amount', 'price']
    show_change_link = True

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class OrderAdmin(admin.ModelAdmin):
    model = Order
    inlines = [OrderItemInline]
    list_display = ['user', 'created_at', 'status']
    readonly_fields = ['user', 'created_at']
    search_fields = ['user']
    list_filter = ['status']


admin.site.register(Order, OrderAdmin)
