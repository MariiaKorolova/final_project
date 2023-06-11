from django.urls import path

from orders.views import OrderDetailView, OrderListView, CartListView, OrderItemDetailView
from orders.views import OrderItemCreateView, OrderItemUpdate, OrderUpdate, OrderConfirm

urlpatterns = [
    path('cart/<int:pk>/order_ok/', OrderItemUpdate.as_view(), name='order_ok'),
    path('cart/<int:pk>/orderupdate/', OrderUpdate.as_view(), name='orderupdate'),
    path('cart/<int:pk>/orderconfirm/', OrderConfirm.as_view(), name='orderconfirm'),

    path('order/<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
    path('order/', OrderListView.as_view(), name='order_list'),
    path('cart/', CartListView.as_view(), name='cart'),
    path('orderitem/<uuid:pk>', OrderItemCreateView.as_view(), name='order_item_add'),
    path('orderitem/<int:pk>/', OrderItemDetailView.as_view(), name='orderitem_detail'),

]