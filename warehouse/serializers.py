from rest_framework import serializers
from books.models import Book, BookItem, Author
from django.contrib.auth.models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username']


class AuthorSerializer(serializers.ModelSerializer):

    books = serializers.HyperlinkedRelatedField(many=True, view_name='book-detail', read_only=True)

    class Meta:
        model = Author
        fields = ['pk', 'first_name', 'last_name', 'date_of_birth', 'date_of_death', 'books']


class BookSerializer(serializers.ModelSerializer):

    bookitem = serializers.HyperlinkedRelatedField(many=True, view_name='bookitem-detail', read_only=True)
    count = serializers.IntegerField(source='books_count', read_only=True)

    class Meta:
        model = Book
        fields = ['pk', 'title', 'id_store', 'price', 'author', 'bookitem', 'count']


class BookItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = BookItem
        fields = "__all__"