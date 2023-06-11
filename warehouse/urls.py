from books.views import BookViewSet, BookItemViewSet, AuthorViewSet
from django.urls import path, include
from rest_framework.routers import DefaultRouter
# from django.views.decorators.cache import cache_page

router = DefaultRouter()
router.register(r'authors', AuthorViewSet, basename="author")
router.register(r'books', BookViewSet, basename="book")
router.register(r'bookitems', BookItemViewSet, basename="bookitem")

urlpatterns = [
    path('', include(router.urls)),
]