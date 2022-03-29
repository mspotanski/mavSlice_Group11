from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum
from _decimal import Decimal
from .models import *
from .forms import *
from django.http import HttpResponseNotFound


def home(request):
    return render(request, 'mavSlice/home.html',
                  {'Home': home})


def register_view(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = RegistrationForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data["username"]
                password = form.cleaned_data["password1"]
                user = authenticate(username=username, password=password)
                login(request, user)
                return redirect("index")
        else:
            form = RegistrationForm()
        context = {"form": form}
        return render(request, 'registration/register.html', context)
    else:
        return redirect("index")


def login_view(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = AuthenticationForm(data=request.POST)
            if form.is_valid():
                username = form.cleaned_data["username"]
                password = form.cleaned_data["password"]
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    if next is not None:
                        return redirect("index")
                    else:
                        return redirect("index")
        else:
            form = AuthenticationForm()
        context = {"form": form}
        return render(request, 'registration/login.html', context)
    else:
        return redirect("index")


def logout_view(request):
        if request.user.is_authenticated:
            logout(request)
        return redirect("index")


def Menu(request):
    return render(request, 'mavSlice/Menu.html',
                  {'Menu': Menu})


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


@login_required
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
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    return redirect('mavSlice:product_list')


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


def add_topping(request):
    pass


def add_product(request):
    pass

