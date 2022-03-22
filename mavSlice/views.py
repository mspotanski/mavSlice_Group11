from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.db.models import Sum
from _decimal import Decimal
from .models import *
from .forms import *

# Do you need a model for every view?
# How to render a request not based on the model?


def home(request):
    return render(request, 'mavSlice/home.html',
                  {'Home': home})


def Menu(request):
    return render(request, 'mavSlice/Menu.html',
                  {'Menu': Menu})


def Cart(request):
    return render(request, 'mavSlice/Cart.html',
                  {'Cart': Cart})


@login_required
def cart_delivery(request):
    return render(request, 'mavSlice/cart_delivery.html',
                  {'Delivery': Delivery})


@login_required
def checkout(request):
    return render(request, 'mavSlice/checkout.html',
                  {'Checkout': checkout})


@login_required
def customer_list(request):
    customer = User.objects.filter()
    return render(request, 'mavSlice/customer_list.html',
                  {'customers': customer})


@login_required
def order_list(request):
    order = Order.objects.filter()
    return render(request, 'mavSlice/order_list.html',
                  {'orders': order})


@login_required
def order_completed_list(request):
    completed_order = Order.objects.filter()
    return render(request, 'mavSlice/order_completed_list.html',
                  {'completed orders': completed_order})


@login_required
def order_not_completed_list(request):
    not_completed_order = Order.objects.filter()
    return render(request, 'mavSlice/order_NOT_completed_list.html',
                  {'Non completed orders': not_completed_order})


@login_required
def order_mark_as_completed(request):
    pass


@login_required
def order_confirmation(request):
    pass


def coupon_list(request):
    coupon = Coupon.objects.filter()
    return render(request, 'mavSlice/coupon_list.html',
                  {'coupons': coupon})


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
def ProductEdit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        # Update
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            product = form.save(commit=False)
            product.updated_date = timezone.now()
            product.save()
            product = Product.objects.filter()
            return render(request, 'mavSlice/product_list.html',
                          {'products': product})
        else:
            # edit
            form = ProductForm(instance=product)
        return render(request, 'mavSlice/ProductEdit.html', {'form': form})


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

