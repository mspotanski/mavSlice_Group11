
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import *


PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'description', 'price')


# NOT FINISHED
class OrdersForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('order_id', 'coupon', 'order_price', 'delivery', 'placed_time', 'completed_time')


# NOT FINISHED
class CouponForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = ('coupon_id', 'totalDiscount',)


class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int)
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)


class DeliveryForm(forms.ModelForm):
    class Meta:
        model = Delivery
        fields = ('street_address', 'street_address2', 'city', 'state', 'zipCode')


