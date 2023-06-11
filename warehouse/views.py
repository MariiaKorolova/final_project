from books.models import Book, BookItem, Author
from books.serializers import BookSerializer, BookItemSerializer, AuthorSerializer
from django.db.models import Count
from rest_framework import viewsets

from rest_framework import permissions


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticated]


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.annotate(books_count=Count('bookitem'))
    serializer_class = BookSerializer


class BookItemViewSet(viewsets.ModelViewSet):
    queryset = BookItem.objects.all()
    serializer_class = BookItemSerializer