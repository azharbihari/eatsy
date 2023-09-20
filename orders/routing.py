from django.urls import re_path, path

from orders.consumers import OrderStatusConsumer

websocket_urlpatterns = [
    path('ws/orders/<int:pk>/status/', OrderStatusConsumer.as_asgi()),
]
