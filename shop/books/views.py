from django.views.generic import ListView, DetailView
from books.models import Author, Book
from orders.models import Order, OrderItem
from django.shortcuts import get_object_or_404
from orders.forms import OrderItemForm


class AuthorsListView(ListView):
    model = Author
    paginate_by = 10
    template_name = 'books/author_list.html'
    ordering = ['first_name']
    queryset = Author.objects.prefetch_related('book_set')


class AuthorDetailView(DetailView):
    model = Author

    def get_context_data(self, **kwargs):
        object_list = Book.objects.filter(author=self.get_object())
        context = super(AuthorDetailView, self).get_context_data(object_list=object_list, **kwargs)
        return context


class BookListview(ListView):
    model = Book
    paginate_by = 10
    template_name = 'books/book_list.html'
    ordering = ['title']
    queryset = Book.objects.select_related('genre').prefetch_related('author')

    def post(self, request, *args, **kwargs):
        pk = request.POST.get('pk')
        book = get_object_or_404(Book, pk=pk)
        orderItem, _ = OrderItem.objects.get_or_create(book_id=book)
        order, _ = Order.objects.get_or_create(user_id=request.user)
        order.order_items.add(orderItem)


class BookDetailView(DetailView):
    model = Book

    def get_context_data(self, **kwargs):
        cart_product_form = OrderItemForm()
        context = super(BookDetailView, self).get_context_data()
        context["cart_product_form"] = cart_product_form
        return context