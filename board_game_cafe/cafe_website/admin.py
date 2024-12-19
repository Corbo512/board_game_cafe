from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Author, Game, Table, Reservation

# Register your models here.

class CustomUserAdmin(UserAdmin):
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'first_name', 'last_name', 'email', 'phone', 'password1', 'password2'),
        }),
    )
    list_display = ('username', 'email', 'first_name', 'last_name','phone', 'is_staff')


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Author)
admin.site.register(Game)
admin.site.register(Table)
admin.site.register(Reservation)
