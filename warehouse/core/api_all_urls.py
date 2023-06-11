from orders.views import OrderViewSet, OrderItemViewSet
from rest_framework.routers import DefaultRouter
from books.views import BookViewSet, BookItemViewSet, AuthorViewSet

router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename="order")
router.register(r'orderitems', OrderItemViewSet, basename="orderitem")
router.register(r'authors', AuthorViewSet, basename="author")
router.register(r'books', BookViewSet, basename="book")
router.register(r'bookitems', BookItemViewSet, basename="bookitem")