from django.contrib import admin
from .models import User, UserSession, UserAddress
from order.models import Order

# Register your models here.


class OrderInline(admin.StackedInline):
    model = Order
    show_change_link = True
    show_full_result_count = True

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class UserAddressInline(admin.TabularInline):
    model = UserAddress
    show_change_link = True
    show_full_result_count = True

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class UserAdmin(admin.ModelAdmin):
    model = User
    readonly_fields = ['user_id',
                       'username', 'phone', 'name', 'language', 'session']
    list_display = ['name', 'phone', 'username']
    search_fields = ['phone', 'username', 'name']
    inlines = [OrderInline, UserAddressInline]

    def has_add_permission(self, request):
        return False


admin.site.register(UserSession)
admin.site.register(User, UserAdmin)
