from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listings(models.Model):
    title = models.CharField(max_length=64)
    imageurl = models.CharField(max_length=128)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=1024)
    category = models.CharField(max_length=32)
    name = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_listings")
    close = models.CharField(max_length=10, default="false")

    def __str__(self):
        return f"{self.title} by {self.name.username}"

class Watchlist(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlistusers")
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name="watchlistlistings")

    def __str__(self):
        return f"{self.username.username} ({self.listing.title})"

class Comments(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment_user")
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name="comment_listing")
    content = models.CharField(max_length=1024)

    def __str__(self):
        return f"{self.content} by {self.name.username}"
