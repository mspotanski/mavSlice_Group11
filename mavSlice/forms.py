from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import *


PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'description', 'price')


class Registration(UserCreationForm):
    email = forms.EmailField(required=True)


class Meta:
    model = User
    fields = ('username', 'fname', 'lname', 'email', 'password1', 'password2', )


def save(self, commit=True):
    User = super(Registration, self).save(commit=False)
    User.fname = self.cleaned_data['fname']
    User.lname = self.cleaned_data['lname']
    User.email = self.cleaned_data['email']

    if commit:
        User.save()

    return User


# NOT FINISHED
class OrdersForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('coupon', 'order_price', 'delivery', 'placed_time')


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


# Not finished, payment info?,
class signupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email',
 #                 'FName', 'LName', 'address', 'State', 'City', 'Zip',
                  'password1', 'password2',)

