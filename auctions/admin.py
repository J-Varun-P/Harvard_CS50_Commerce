from django.contrib import admin

from .models import User, Listings, Watchlist, Bid, Comments, CloseAuction

# Register your models here.

admin.site.register(User)
admin.site.register(Listings)
admin.site.register(Watchlist)
admin.site.register(Bid)
admin.site.register(Comments)
admin.site.register(CloseAuction)
