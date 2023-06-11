from django.contrib import admin
from orders.models import Book, BookItem, OrderItem
from models import Author


class OrderItemInline(admin.StackedInline):
    model = OrderItem
    extra = 1


class BookInline(admin.StackedInline):
    model = Book
    extra = 1


class BookItemInline(admin.StackedInline):
    model = OrderItem
    extra = 1


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    inlines = [BookInline]
    list_display = ('first_name', 'last_name', 'date_of_birth', 'date_of_death')


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline, BookItemInline]

    list_display = ('title', 'id_store', 'price', 'author')
    list_filter = ['title', 'author']


@admin.register(BookItem)
class BookItemAdmin(admin.ModelAdmin):
    list_display = ('isbn', 'book_id', 'row', 'shelf', 'history')
    list_filter = ['book_id', 'history']