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
        return f"{self.title}"
