from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db import models
from django.contrib.auth.models import User
from restaurants.models import Menu, Restaurant
from django.contrib.auth import get_user_model

User = get_user_model()


class Order(models.Model):

    ORDER_STATUS = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('preparing', 'Preparing'),
        ('out_for_delivery', 'Out for Delivery'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    items = models.ManyToManyField(Menu, through='OrderItem')
    total_amount = models.DecimalField(max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    is_delivered = models.BooleanField(default=False)
    status = models.CharField(
        max_length=20, choices=ORDER_STATUS, default='pending')

    def __str__(self):
        return f"Order #{self.pk} for {self.restaurant.name} by {self.user.username}"

    class Meta:
        ordering = ['-created_at']


class OrderItem(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} x {self.menu.name} in Order #{self.order.pk}"


@receiver(post_save, sender=Order)
def order_status_updated(sender, instance, **kwargs):
    from channels.layers import get_channel_layer
    from asgiref.sync import async_to_sync
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f'order_{instance.pk}',
        {
            'type': 'update.order.status',
            'status': instance.get_status_display()
        }
    )
