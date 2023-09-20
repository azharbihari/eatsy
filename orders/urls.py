from django.urls import path
from orders.views import PlaceOrderView, OrderListView, OrderDetailView

urlpatterns = [
    path('', OrderListView.as_view(), name='order-list'),
    path('<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('<slug:slug>/place_order', PlaceOrderView.as_view(), name='place-order'),

]
