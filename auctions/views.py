from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listings, Watchlist, Comments, Bid


def index(request):
    print(request.user)
    listings = Listings.objects.filter(close="false").all()
    for l in listings:
        print(l, l.name.username, l.id)
    return render(request, "auctions/index.html", {
    "listings": listings
    })


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
        #print(request.user.username, request.POST["category"])
        username = request.user.username
        #print(request.POST["title"], request.POST["urlname"], request.POST["price"], request.POST["description"])
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
        username = User.objects.get(pk=request.user.id)
        listing = Listings(title=request.POST["title"], imageurl=request.POST["urlname"], price=request.POST["price"], description=request.POST["description"], category=request.POST["category"], name=username)
        listing.save()
        return HttpResponseRedirect(reverse("index"))
        #print(listing, listing.name)
        #return HttpResponse("Hello")
    else:
        return render(request, "auctions/addlisting.html")


def listings(request, id):
    """
    print(request.user.username)
    listing = Listings.objects.get(pk=id)
    print(listing)
    list = Listings.objects.get(pk=id)
    print(list)
    obj = list.name.all().first()
    print(obj.email, obj.username)
    return render(request, "auctions/listings.html", {
    "listing": listing, "username": obj.username
    })

    """
    listing = Listings.objects.get(pk=id)
    username = listing.name.username
    comments = Comments.objects.filter(listing=listing)
    bid = Bid.objects.filter(listing=listing).first()
    if bid is None:
        check = "false"
    else:
        bid_success = Bid.objects.get(listing=listing)
        check = "true"
    return render(request, "auctions/listings.html", {
    "listing": listing, "username": username, "comments": comments, "check": check, "bid_success": bid_success
    })

def watchlist_id(request, id):
    listing = Listings.objects.get(pk=id)
    print(listing)
    user = User.objects.get(username=request.user.username)
    c_list = Watchlist.objects.filter(username=request.user)
    for c in c_list:
        print(c)
        if listing == c.listing:
            print("You have already added this to your watchlist")
            return HttpResponseRedirect(reverse("watchlist"))
    w_list = Watchlist(username=user, listing=listing)
    print(w_list)
    w_list.save()
    return HttpResponseRedirect(reverse("watchlist"))


def watchlist(request):
    """
    print(Watchlist.objects.filter(username=request.user).all())
    return HttpResponse("Hello")
    print(Watchlist.objects.filter(username=request.user).all())
    """
    listings = Watchlist.objects.filter(username=request.user).all()
    return render(request, "auctions/watchlist.html", {
    "listings": listings
    })

def removewatchlist(request, id):
    listing = Listings.objects.get(pk=id)
    Watchlist.objects.filter(listing=listing).delete()
    return HttpResponseRedirect(reverse("watchlist"))

def selectcategory(request):
    return render(request, "auctions/selectcategory.html")

def categories(request):
    category = request.POST["category"]
    listings = Listings.objects.filter(category=category).all()
    return render(request, "auctions/categories.html", {
    "listings": listings
    })

def addcomment(request, id):
    listing = Listings.objects.get(pk=id)
    name = User.objects.get(username=request.user.username)
    content = request.POST["comment"]
    if content != "":
        print(f"{name}, {listing}, {content}")
        comment = Comments(name=name,listing=listing,content=content)
        comment.save()
    return HttpResponseRedirect(reverse("listings", args=(listing.id,)))

def addmybid(request, id):
    listing = Listings.objects.get(pk=id)
    name = User.objects.get(username=request.user.username)
    comments = Comments.objects.filter(listing=listing)

    bid = Bid.objects.filter(listing=listing).first()
    if bid is None:
        check = "false"
    else:
        bid_success = Bid.objects.get(listing=listing)
        check = "true"

    bid_amount = request.POST["bid"]
    if bid_amount == "":
        return HttpResponseRedirect(reverse("listings", args=(listing.id,)))
    try:
        float(request.POST["bid"])
    except ValueError:
        comments = Comments.objects.filter(listing=listing)
        return render(request, "auctions/listings.html", {
        "listing": listing, "username": listing.name.username, "comments": comments, "message": "Please provide a real number for the bid amount", "bid_success": bid_success, "check": check
        })
    current_bid = Bid.objects.filter(listing=listing).first()
    print(current_bid)
    bid_amount = float(bid_amount)
    print(f"float {bid_amount} current bid {current_bid.bid_amount}")
    bid = Bid(bid_amount=bid_amount, name=name, listing=listing)
    if current_bid is None:
        if bid_amount > listing.price:
            print(bid_amount, listing.price)
            bid.save()
            return render(request, "auctions/listings.html", {
            "listing": listing, "username": listing.name.username, "comments": comments, "bid_success": bid, "message1": "Bid Successfully placed", "check": "true"
            })
        else:
            return render(request, "auctions/listings.html", {
            "listing": listing, "username": listing.name.username, "comments": comments, "message": "Please bid higher than the original price", "bid_success": bid, "check": "false"
            })
    else:
        if bid_amount <= current_bid.bid_amount:
            return render(request, "auctions/listings.html", {
            "listing": listing, "username": listing.name.username, "comments": comments, "message": "Please bid higher than the current bid", "check": "true", "bid_success": bid_success
            })
        else:
            print(current_bid.bid_amount, bid_amount)
            current_bid.bid_amount = bid_amount
            current_bid.name = request.user
            return render(request, "auctions/listings.html", {
            "listing": listing, "username": listing.name.username, "comments": comments, "bid_success": current_bid, "message1": "Bid Successfully placed", "check": "true"
            })
    return HttpResponse("You're here")
    pass
