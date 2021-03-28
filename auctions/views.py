from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listings, Watchlist, Comments, Bid, CloseAuction


def index(request):
    notactive = CloseAuction.objects.all()
    notactivelist = []
    wonlist = []
    short_desc = [] # for short description in active listings
    for object in notactive:
        notactivelist.append(object.listing)
        print(object.listing)
    listings = Listings.objects.filter(close="false").all()
    for l in listings:
        short_desc.append(l.description.splitlines()[0])
        print(l.description.splitlines()[0])
        # checking if the listing is closed
        a = Bid.objects.filter(listing=l).first()
        if a is not None:
            # checking if the current user won the listing if the listing is closed
            b = l.bid_listing.all().first()
            c = b.name.username
            if c == request.user.username:
                wonlist.append(l)
    combined_list = zip(listings, short_desc)
    return render(request, "auctions/index.html", {
    "combined_list": combined_list, "notactive": notactivelist, "wonlist": wonlist
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

@login_required
def addlisting(request):
    if request.method == "POST":
        username = request.user.username
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
    else:
        return render(request, "auctions/addlisting.html")

@login_required
def listings(request, id):
    listing = Listings.objects.get(pk=id)
    username = listing.name.username
    comments = Comments.objects.filter(listing=listing)
    bid = Bid.objects.filter(listing=listing).first()
    closeauction = CloseAuction.objects.filter(listing=listing).first()
    if closeauction is None:
        close_bidding = "no"
    else:
        close_bidding = "yes"
    if bid is None:
        check = "false"
    else:
        check = "true"
    return render(request, "auctions/listings.html", {
    "listing": listing, "username": username, "comments": comments, "check": check, "bid_success": bid, "close_bidding": close_bidding
    })

@login_required
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

@login_required
def watchlist(request):
    listings = Watchlist.objects.filter(username=request.user).all()
    short_desc = []
    for l in listings:
        short_desc.append(l.listing.description.splitlines()[0])
    combined_list = zip(listings, short_desc)
    return render(request, "auctions/watchlist.html", {
    "combined_list": combined_list
    })

@login_required
def removewatchlist(request, id):
    listing = Listings.objects.get(pk=id)
    Watchlist.objects.filter(listing=listing).delete()
    return HttpResponseRedirect(reverse("watchlist"))

@login_required
def selectcategory(request):
    return render(request, "auctions/selectcategory.html")

@login_required
def categories(request):
    category = request.POST["category"]
    listings = Listings.objects.filter(category=category).all()
    short_desc = []
    for l in listings:
        short_desc.append(l.description.splitlines()[0])
    combined_list = zip(listings, short_desc)
    return render(request, "auctions/categories.html", {
    "combined_list": combined_list
    })

@login_required
def addcomment(request, id):
    listing = Listings.objects.get(pk=id)
    name = User.objects.get(username=request.user.username)
    content = request.POST["comment"]
    if content != "":
        print(f"{name}, {listing}, {content}")
        comment = Comments(name=name,listing=listing,content=content)
        comment.save()
    return HttpResponseRedirect(reverse("listings", args=(listing.id,)))

@login_required
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
        return render(request, "auctions/listings.html", {
        "listing": listing, "username": listing.name.username, "comments": comments, "message": "Please provide a real number for the bid amount", "bid_success": bid, "check": check, "close_bidding": "no"
        })
    bid_amount = float(bid_amount)
    bid1 = Bid(bid_amount=bid_amount, name=name, listing=listing)
    if bid is None:
        if bid_amount > listing.price:
            print(bid_amount, listing.price)
            bid1.save()
            return render(request, "auctions/listings.html", {
            "listing": listing, "username": listing.name.username, "comments": comments, "bid_success": bid1, "message1": "Bid Successfully placed", "check": "true", "close_bidding": "no"
            })
        else:
            return render(request, "auctions/listings.html", {
            "listing": listing, "username": listing.name.username, "comments": comments, "message": "Please bid higher than the original price", "bid_success": bid, "check": "false", "close_bidding": "no"
            })
    else:
        if bid_amount <= bid.bid_amount:
            return render(request, "auctions/listings.html", {
            "listing": listing, "username": listing.name.username, "comments": comments, "message": "Please bid higher than the current bid", "check": "true", "bid_success": bid, "close_bidding": "no"
            })
        else:
            print(bid.bid_amount, bid_amount)
            bid.bid_amount = bid_amount
            bid.name = request.user
            bid.save()
            return render(request, "auctions/listings.html", {
            "listing": listing, "username": listing.name.username, "comments": comments, "bid_success": bid, "message1": "Bid Successfully placed", "check": "true", "close_bidding": "no"
            })


@login_required
def closeauction(request, id):
    listing = Listings.objects.get(pk=id)
    username = listing.name.username
    comments = Comments.objects.filter(listing=listing)
    bid = Bid.objects.filter(listing=listing).first()

    closeauction = CloseAuction(listing=listing)
    closeauction.save()
    return render(request, "auctions/listings.html", {
    "listing": listing, "username": username, "comments": comments, "bid_success": bid, "close_bidding": "yes"
    })

@login_required
def reopenauction(request, id):
    listing = Listings.objects.get(pk=id)
    reopenauction = CloseAuction.objects.get(listing=listing)
    print(reopenauction)
    reopenauction.delete()
    return HttpResponseRedirect(reverse("listings", args=(listing.id,)))
