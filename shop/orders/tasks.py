import os
from celery import shared_task
from django.core.mail import send_mail
import requests
from orders.models import Order
from orders.models import OrderItem


@shared_task
def send(email, text_reminder):
    if text_reminder == 'ordered':
        send_mail(
            'Reminder',
            text_reminder,
            'gontarevsanya@example.com',
            [email, ],
            fail_silently=False,
        )


@shared_task
def get_order(obj, email):
    token = os.environ.get('TOKEN_SECRET')
    headers = {'Authorization': 'Token {}'.format(token)}
    order = Order.objects.get(pk=obj.pk)
    user_email = email
    request_obj = {
        "delivery_address": order.delivery_address,
        "status": "i",
        "user_email": user_email,
        "order_id_in_shop": order.pk,
    }
    try:
        url = "http://warehouse:8000/api/orders/"
        token = os.environ.get('TOKEN_SECRET')
        headers = {'Authorization': 'Token {}'.format(token)}
        response = requests.post(url=url, json=request_obj, headers=headers)
        print("Status Code", response.status_code)
        print("JSON Response ", response.json())
    except Exception as e:
        print(e)

    response1 = requests.get(url=url, headers=headers)
    order_item_all = OrderItem.objects.filter(order_id=obj.pk)
    for order_warehouse in response1.json()['results']:
        if order_warehouse['order_id_in_shop'] == obj.pk:
            for order_shop in order_item_all:
                order_items = {

                    "quantity": order_shop.quantity,
                    "book_id": str(order_shop.book_id.pk),
                    "order_id": order_warehouse['pk'],
                    "book_item_id": [1]
                }
                try:
                    headers = {'Authorization': 'Token {}'.format(token)}
                    response2 = requests.post(url="http://warehouse:8000/api/orderitems/",
                                              json=order_items,
                                              headers=headers)
                    print("Status Code", response2.status_code)
                    print("JSON Response ", response2.json())
                except Exception as e:
                    print(e)