from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, DeleteView
from carts.models import CartItem, Cart
from restaurants.models import Menu
from django.views.generic.detail import SingleObjectMixin
from django.views import View
from django.http import HttpResponseRedirect
from django.contrib import messages


class AddToCartView(LoginRequiredMixin, SingleObjectMixin, View):
    model = Menu

    def post(self, request, *args, **kwargs):
        menu = self.get_object()
        quantity = request.POST.get('quantity', 1)
        cart, _ = Cart.objects.get_or_create(user=self.request.user)

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart, menu=menu)

        if not created:
            cart_item.quantity += int(quantity)
            cart_item.save()
            messages.success(
                request, f"Quantity of {menu.name} increased to {cart_item.quantity}.")
        else:
            cart_item.quantity = int(quantity)
            cart_item.save()
            messages.success(request, "Item added to the cart.")

        return HttpResponseRedirect(
            reverse('restaurant-detail',
                    kwargs={'slug': menu.restaurant.slug})
        )


class RemoveFromCartView(LoginRequiredMixin, SingleObjectMixin, View):
    model = CartItem

    def get(self, request, *args, **kwargs):
        cart_item = self.get_object()
        if cart_item.cart.user != self.request.user:
            messages.error(
                request, "You don't have permission to remove this item from the cart.")
            return HttpResponseRedirect(
                reverse('restaurant-detail',
                        kwargs={'slug': cart_item.menu.restaurant.slug})
            )

        cart_item.delete()
        messages.success(request, "Item removed from the cart.")
        return HttpResponseRedirect(
            reverse('restaurant-detail',
                    kwargs={'slug': cart_item.menu.restaurant.slug})
        )
