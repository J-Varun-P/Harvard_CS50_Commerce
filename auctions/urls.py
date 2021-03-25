from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("addlisting", views.addlisting, name="addlisting"),
    path("listings/<int:id>", views.listings, name="listings"),
    path("listings/watchlist/<int:id>", views.watchlist_id, name="watchlist_id"),
    path("listings/watchlist", views.watchlist, name="watchlist"),
    path("listings/removewatchlist/<int:id>", views.removewatchlist, name="removewatchlist"),
    path("selectcategory", views.selectcategory, name="selectcategory"),
    path("categories", views.categories, name="categories"),
    path("addcomment/<int:id>", views.addcomment, name="addcomment")
]
