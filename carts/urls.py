from django.urls import path
from carts.views import AddToCartView, RemoveFromCartView

urlpatterns = [
    path("<int:pk>/add_to_cart", AddToCartView.as_view(), name="add-to-cart"),
    path("<int:pk>/remove_from_cart",
         RemoveFromCartView.as_view(), name="remove-from-cart"),
]
