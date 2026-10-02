from django.contrib import admin

from .models import Booking, Category, MenuItem

admin.site.register(Category)
admin.site.register(MenuItem)
admin.site.register(Booking)
