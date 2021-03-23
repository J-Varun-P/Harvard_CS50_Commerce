from django.contrib import admin

from .models import User, Listings

# Register your models here.

admin.site.register(User)
admin.site.register(Listings)
