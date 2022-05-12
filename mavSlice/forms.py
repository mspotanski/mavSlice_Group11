from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import *
from django.contrib.auth.models import User


PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'description', 'price', 'image')


# class Registration(UserCreationForm):
#     email = forms.EmailField(required=True)


# class UserForm(forms.ModelForm):
#     class Meta:
#         model = User
#         #fields = ('username', 'fname', 'lname', 'email', 'password1', 'password2', )
#         fields = ('first_name', 'last_name', 'email')

# class CustomerForm(forms.ModelForm):
#     class Meta:
#         model = customer
#         fields = ('cust_fname', 'cust_lname', 'cust_password', 'delivery_info','payment_info')


# def save(self, commit=True):
#     customer = super(Registration, self).save(commit=False)
#     customer.fname = self.cleaned_data['fname']
#     customer.lname = self.cleaned_data['lname']
#     #customer.email = self.cleaned_data['email']
#
#    if commit:
#        User.save()
#        customer.save()
#        return customer


# NOT FINISHED
# class OrdersForm(forms.ModelForm):
#     class Meta:
#         model = Order
#         fields = ('coupon', 'order_price', 'delivery', 'placed_time')
class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address', 'state',
                  'city', 'zip',]


# NOT FINISHED
class CouponForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = ('totalDiscount',)


class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int)
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)


# class DeliveryForm(forms.ModelForm):
#     class Meta:
#         model = Delivery
#         fields = ('street_address', 'street_address2', 'city', 'state', 'zipCode')


# Not finished, payment info?,
# class signupForm(UserCreationForm):
    # delivery_info = forms.ModelForm()
    # payment_info = forms.ModelForm()
    # delivery_info = forms.ModelForm()

class User(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password1',)

