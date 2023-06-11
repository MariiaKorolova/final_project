import os

from celery import shared_task
from django.core.mail import send_mail
import requests
from books.models import Book, Author


@shared_task
def send(email, text_reminder):
    send_mail(
        'Reminder',
        text_reminder,
        'gontarevsanya@example.com',
        [email, ],
        fail_silently=False,
    )


@shared_task
def get_count():
    try:
        url = "http://warehouse:8000/api/books/"
        token = os.environ.get('TOKEN_SECRET')
        response = requests.get(url, headers={'Authorization': 'Token ' + token})
        parsed = response.json()
        for i in parsed['results']:
            book_id_warehouse = i['id_store']
            find_book = Book.objects.filter(id_in_store=book_id_warehouse)
            if find_book:
                book_in_shop = find_book[0]
                book_in_shop.quantity = i['count']
                book_in_shop.price = i['price']
                book_in_shop.save()
            else:
                book_in_shop = Book()
                author_book = Author()

                author_book.first_name = i['author']['first_name']
                author_book.last_name = i['author']['last_name']
                author_book.date_of_birth = i['author']['date_of_birth']
                author_book.date_of_death = i['author']['date_of_death']
                author_book.save()

                book_in_shop.id_in_store = i['id_store']
                book_in_shop.title = i['title']
                book_in_shop.price = i['price']
                book_in_shop.author = author_book
                book_in_shop.quantity = i['count']
                book_in_shop.save()
    except Exception as e:
        print(e)