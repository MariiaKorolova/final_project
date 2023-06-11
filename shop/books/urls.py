from django.urls import path
from books import views
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('books/', cache_page(60*10)(views.BookListview.as_view()), name='book-list'),
    path('books/<uuid:pk>', cache_page(60*10)(views.BookDetailView.as_view()), name='book-detail'),
    path('authors/', cache_page(60*10)(views.AuthorsListView.as_view()), name='author-list'),
    path('authors/<int:pk>', cache_page(60*10)(views.AuthorDetailView.as_view()), name='author-detail'),
]