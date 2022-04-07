from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect
from django.views.decorators.http import require_POST
from .models import *
from .forms import *
from .cart import *

from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponseNotFound


def home(request):
    return render(request, 'mavSlice/home.html',
                  {'Home': home})


def Menu(request):
    return render(request, 'mavSlice/Menu.html',
                  {'Menu': Menu})


def custom(request):
    return render(request, 'mavSlice/custom.html',
                  {'custom': custom})


# Cart Functionality
def Cart_view(request):
    # price_all = Decimal(calculate_cart_price(request.user))
    # context = {}
    # context.update ({"price_all": price_all})
    # context.update({"Pizza": Product.objects.filter(add_by=request.user).filter(already_ordered=False)})
    return render(request, 'mavSlice/Cart.html',
                  {'Cart': Cart_view})


# Context Processor
# May need its own .py file
def cart(request):
    return {'cart': Cart(request)}


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 update_quantity=cd['update'])
    return redirect('mavSlice/Cart.html')


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('mavSlice/Cart.html')


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'], 'update': True})
    return render(request, 'mavSlice/Cart.html', {'cart': cart})


def product_detail(request, id):
    product = get_object_or_404(Product, id=id, available=True)
    cart_product_form = CartAddProductForm()
    return render(request, 'mavSlice/product_detail.html',
                  {'product': product, 'cart_product_form': cart_product_form})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
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
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


# def calculate_cart_price(username):
# price_all = 0
# for obj in Product.objects.filter(add_by=username).filter(already_ordered=False):
# price_all += obj.price
# return price_all

# Order Functionality
def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrdersForm(request.POST)
        if form.is_valid():
            order = form.save()
            for product in cart:
                OrderProduct.objects.create(order=order, product=product['product'], price=product['price'],
                                            quantity=product['quantity'])
            # clear the cart
            cart.clear()
            # set the order in the session
            request.session['order_id'] = order.order_id
            # redirect for payment
            return redirect(reverse('mavSlice:process_payment'))

    else:
        form = OrdersForm()
    return render(request,
                  'mavSlice/Cart.html',
                  {'cart': cart, 'form': form})


@staff_member_required
# NOT AN ACTUAL STAFF MEMBER ACCOUNT
# ONLY SHOWS UP ON ADMIN SIDE
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request,
                  'admin/admin_order_detail.html',
                  {'order': order})


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


