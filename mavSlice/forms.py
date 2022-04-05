
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User, Product, Coupon, Order


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'email')


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('username', 'email')


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'description', 'price')


# NOT FINISHED
# class ToppingsForm(forms.ModelForm):
#     class Meta:
#         model = Toppings
#         fields = ('name',)


# NOT FINISHED
class OrdersForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('order_id', 'customer', 'products', 'coupon', 'order_price', 'delivery',)


# NOT FINISHED
class CouponForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = ('coupon_id', 'totalDiscount',)
