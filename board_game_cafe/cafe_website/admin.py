from django.contrib import admin
from .models import User, Author, Game, Table, Reservation

# Register your models here.

admin.site.register(User)
admin.site.register(Author)
admin.site.register(Game)
admin.site.register(Table)
admin.site.register(Reservation)
