from django import forms
from orders import models


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = models.OrderItem
        fields = ['quantity']