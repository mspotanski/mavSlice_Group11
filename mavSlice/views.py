from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.db.models import Sum
from _decimal import Decimal
from .models import *
from .forms import *


def home(request):
    return render(request, 'mavSlice/home.html',
                  {'Home': home})


def Menu(request):
    return render(request, 'mavSlice/Menu.html',
                  {'Menu': Menu})


@login_required
def Cart(request):
    pass


def cart_delivery(request):
    pass


def checkout(request):
    pass


@login_required
def customer_list(request):
    customer = User.objects.filter()
    return render(request, 'mavSlice/customer_list.html',
                  {'customers': customer})


@login_required
def order_list(request):
    pass


@login_required
def order_completed_list(request):
    pass


@login_required
def order_NOT_completed_list(request):
    pass


@login_required
def order_mark_as_completed(request):
    pass


@login_required
def order_confirmation(request):
    pass


def coupon_list(request):
    pass


@login_required
def coupon_new(request):
    pass


@login_required
def coupon_edit(request):
    pass


@login_required
def product_list(request):
    pass


@login_required
def product_info(request):
    pass


@login_required
def product_new(request):
    pass


@login_required
def ProductEdit(request):
    pass


@login_required
def product_delete(request):
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

