from django.db import models
from books.models import BookItem, Book


class Order(models.Model):
    user_email = models.EmailField(max_length=254)

    ORDER_STATUS = (
        ('i', 'In_work'),
        ('s', 'Success'),
        ('f', 'Fail'),
    )

    status = models.CharField(max_length=1, choices=ORDER_STATUS, blank=True, default='i', help_text='Order status')
    delivery_address = models.CharField(max_length=255, help_text='delivery address')
    order_id_in_shop = models.IntegerField(null=True, unique=True)

    def __str__(self):
        return str(self.pk)


class OrderItem(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='orderitem')
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='book')
    quantity = models.IntegerField()
    book_item_id = models.ManyToManyField(BookItem)

    def __str__(self):
        return str(self.pk)