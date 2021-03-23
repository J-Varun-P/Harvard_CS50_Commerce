from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listings(models.Model):
    title = models.CharField(max_length=64)
    imageurl = models.CharField(max_length=128)
    price = models.IntegerField()
    description = models.CharField(max_length=1024)
    category = models.CharField(max_length=32)
    name = models.ManyToManyField(User, related_name="user_listings")
    close = models.CharField(max_length=10, default="false")

    def __str__(self):
        return f"{self.title}"
