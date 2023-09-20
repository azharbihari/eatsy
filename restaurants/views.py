from restaurants.models import Restaurant
from django.views.generic import DetailView, ListView
from carts.models import CartItem


class RestaurantListView(ListView):
    model = Restaurant
    paginate_by = 10


class RestaurantDetailView(DetailView):
    model = Restaurant

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_authenticated:
            cart_items = CartItem.objects.filter(
                cart__user=user,
                menu__restaurant=self.object
            )

            total_amount = sum(
                item.quantity * item.menu.price for item in cart_items)

            context['cart_items'] = cart_items
            context['total_amount'] = total_amount
        return context
