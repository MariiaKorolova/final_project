from django.db import models
from users.models import User
from books.models import Book
from django.urls import reverse


class Order(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    ORDER_STATUS = (
        ('cart', 'Cart'),
        ('ordered', 'Ordered'),
        ('success', 'Success'),
        ('fail', 'Fail'),
    )

    status = models.CharField(max_length=10, choices=ORDER_STATUS, blank=True, default='cart',
                              help_text='If you confirm, choose ordered')
    delivery_address = models.CharField(max_length=255, default='input address')

    def __str__(self):
        return str(self.pk)


def get_absolute_url():
    return reverse('order_list')


class OrderItem(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, related_name='orders111')
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE, null=True, related_name='books111')
    quantity = models.IntegerField()

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse('order_list')