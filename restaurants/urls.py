from django.urls import path
from restaurants.views import RestaurantListView, RestaurantDetailView

urlpatterns = [
    path("", RestaurantListView.as_view(), name="restaurant-list"),
    path("<slug:slug>/", RestaurantDetailView.as_view(), name="restaurant-detail"),
]
