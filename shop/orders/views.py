from django.views.generic import ListView, DetailView, CreateView, View, UpdateView
from orders.models import Order, OrderItem
from books.models import Book
from django.shortcuts import reverse
from books.tasks import send
from orders.tasks import get_order
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404


class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    paginate_by = 10
    template_name = 'orders/order_list.html'

    def get_queryset(self):
        queryset = Order.objects.filter(user_id=self.request.user)
        return queryset


class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'orders/order_detail.html'


class OrderItemDetailView(LoginRequiredMixin, DetailView):
    model = OrderItem
    template_name = 'orders/orderitem_detail.html'


class OrderView(View):
    model = Order
    paginate_by = 5

    def get_queryset(self):
        queryset = Order.objects.filter(status='cart').select_related("user_id")
        return queryset


class CartListView(ListView):
    model = OrderItem
    paginate_by = 2
    template_name = 'orders/cart.html'

    def get_queryset(self):
        queryset = OrderItem.objects.select_related("order_id").filter(order_id__user_id=self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        context["order"] = Order.objects.get(user_id=self.request.user)
        return context


class OrderItemCreateView(LoginRequiredMixin, CreateView):
    model = OrderItem
    fields = ['quantity', 'book_id', 'order_id']
    template_name = 'orders/order_item_add.html'

    def get_initial(self, *args, **kwargs):
        initial = super(OrderItemCreateView, self).get_initial()
        initial['book_id'] = get_object_or_404(Book, pk=self.kwargs['pk'])
        order, _ = Order.objects.get_or_create(user_id=self.request.user)
        initial['order_id'] = order
        return initial


class OrderUpdate(LoginRequiredMixin, UpdateView):
    model = Order
    template_name = 'orders/orderupdate.html'
    fields = ['delivery_address']

    def get_success_url(self):
        pk = self.kwargs["pk"]
        return reverse("order_detail", kwargs={"pk": pk})


class OrderItemUpdate(LoginRequiredMixin, UpdateView):
    model = OrderItem
    template_name = 'orders/order_ok.html'
    fields = ['quantity']

    def get_success_url(self):
        pk = self.kwargs["pk"]
        return reverse("orderitem_detail", kwargs={"pk": pk})


class OrderConfirm(LoginRequiredMixin, UpdateView):
    model = Order
    template_name = 'orders/orderconfirm.html'
    fields = ['status']

    def form_valid(self, form):
        self.object = form.save(commit=False)
        obj = self.get_object()
        email = self.request.user.email
        obj.status = 'ordered'
        text_reminder = f'{obj.status} {self.object}'
        send(email=email, text_reminder=text_reminder)
        get_order(obj, email)

        obj.save()
        return super(OrderConfirm, self).form_valid(form)

    def get_success_url(self):
        pk = self.kwargs["pk"]
        return reverse("order_detail", kwargs={"pk": pk})