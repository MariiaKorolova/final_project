from rest_framework import serializers
from orders.models import Order, OrderItem
from django.contrib.auth.models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class OrderSerializer(serializers.ModelSerializer):
    orderitem = serializers.HyperlinkedRelatedField(
        view_name='orderitem-detail',
        many=True,
        queryset=OrderItem.objects.all(),
    )

    class Meta:
        model = Order
        fields = ['pk', 'status', 'delivery_address', 'user_email', 'order_id_in_shop', 'orderitem']


class OrderItemSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        super(OrderItemSerializer, self).__init__(*args, **kwargs)
        if 'view' in self.context and self.context['view'].action != 'create':
            self.fields.update({"order_id": OrderSerializer()})

    class Meta:
        model = OrderItem
        fields = ['id', 'quantity', 'book_id', 'order_id', 'book_item_id']