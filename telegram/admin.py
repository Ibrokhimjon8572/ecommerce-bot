from django.contrib import admin
from .models import User

# Register your models here.


class UserAdmin(admin.ModelAdmin):
    model = User
    readonly_fields = ['user',
                       'username', 'phone', 'name', 'language']
    list_display = ['name', 'phone', 'username']

    def has_add_permission(self, request):
        return False


admin.site.register(User, UserAdmin)
