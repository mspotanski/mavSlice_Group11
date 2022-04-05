from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum
from _decimal import Decimal
from .models import *
from .forms import signupForm
from django.http import HttpResponseNotFound
from django.views.generic import TemplateView



def home(request):
    return render(request, 'mavSlice/home.html',
                  {'Home': home})


def Menu(request):
    return render(request, 'mavSlice/Menu.html',
                  {'Menu': Menu})


def custom(request):
    return render(request, 'mavSlice/custom.html',
                  {'custom': custom})


def signup(request):
    if request.method == 'POST':
        form = signupForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            # load the profile instance created by the signal
            user.save()
            raw_password = form.cleaned_data.get('password1')

            # login user after signing up
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)

            # redirect user to home page
            return redirect('home')
    else:
        form = signupForm()
    return render(request, 'registration/signup.html', {'form': form})


def Cart(request):
    # price_all = Decimal(calculate_cart_price(request.user))
    # context = {}
    # context.update ({"price_all": price_all})
    # context.update({"Pizza": Product.objects.filter(add_by=request.user).filter(already_ordered=False)})
    return render(request, 'mavSlice/Cart.html',
                  {'Cart': Cart})


# def calculate_cart_price(username):
    # price_all = 0
    # for obj in Product.objects.filter(add_by=username).filter(already_ordered=False):
        # price_all += obj.price
    # return price_all


@login_required
def cart_delivery(request):
    return render(request, 'mavSlice/cart_delivery.html',
                  {'Delivery': Delivery})


@login_required
def checkout(request):
    return render(request, 'mavSlice/checkout.html',
                  {'Checkout': checkout})


@login_required
def order_confirmation(request):
    pass


@login_required
def user_info(request):
    pass


@login_required
def user_info_delivery(request):
    pass


@login_required
def user_info_payment(request):
    pass


def determine_order_price(request):
    pass


def add_product(request):
    pass


def update_order(request):
    pass

