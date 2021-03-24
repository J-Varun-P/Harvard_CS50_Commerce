from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listings


def index(request):
    print(request.user)
    listings = Listings.objects.filter(close="false").all()
    print(listings)
    return render(request, "auctions/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def addlisting(request):
    if request.method == "POST":
        print(request.user.username, request.POST["category"])
        username = request.user.username
        print(request.POST["title"], request.POST["urlname"], request.POST["price"], request.POST["description"])
        if request.POST["title"] == "" or request.POST["urlname"] == ""  or request.POST["description"] == "" or request.POST["price"] == "":
            return render(request, "auctions/addlisting.html", {
            "message": "Please fill the form completely to add a listing"
            })
        try:
            float(request.POST["price"])
        except ValueError:
            return render(request, "auctions/addlisting.html", {
            "message": "Please provide a real number for the price tag"
            })
    return render(request, "auctions/addlisting.html")


def listings(request, id):
    print(request.user.username)
    listing = Listings.objects.filter(pk=id).first()
    user = request.user.username
    userlistings = user.user_listings.all()
    for u in userlistings:
        print(u)
    print(listing.name)
    return render(request, "auctions/listings.html", {
    "listing": listing
    })
