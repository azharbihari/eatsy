from django.urls import reverse, reverse_lazy
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from restaurants.models import Restaurant
from carts.models import CartItem
from orders.models import Order, OrderItem
from django.views import View
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.views.generic import DetailView, ListView


class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    paginate_by = 10

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order


class PlaceOrderView(LoginRequiredMixin, SingleObjectMixin, View):
    model = Restaurant

    def post(self, request, *args, **kwargs):
        restaurant = self.get_object()
        user = self.request.user

        order = Order.objects.create(
            user=user,
            restaurant=restaurant,
            total_amount=0
        )

        cart_items = CartItem.objects.filter(
            cart__user=user, menu__restaurant=restaurant)

        for cart_item in cart_items:
            OrderItem.objects.create(
                menu=cart_item.menu,
                order=order,
                quantity=cart_item.quantity
            )
            order.total_amount += cart_item.menu.price * cart_item.quantity
            cart_item.delete()

        order.save()
        messages.success(request, "Your order has been placed successfully!")

        return HttpResponseRedirect(
            reverse('restaurant-detail',
                    kwargs={'slug': restaurant.slug})
        )
