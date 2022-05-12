from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from django.template.loader import render_to_string
from .models import *
from .forms import *
from .cart import *
from .forms import *
import braintree
from django.core.mail import send_mail
from django.conf import settings


# import weasyprint


# Menu Functionality
def Menu(request):
    products = Product.objects.filter(type__exact='Whole Pie')
    return render(request, 'mavSlice/Menu.html', {'products': products})


def slice_Menu(request):
    products = Product.objects.filter(type__exact='Slice')
    return render(request, 'mavSlice/slice_Menu.html', {'products': products})


def get_products():
    return Product.objects.filter(created_date__lte=timezone.now())


def home(request):
    return render(request, 'mavSlice/home.html',
                  {'Home': home})


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
    product = get_object_or_404(Product, product_id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 update_quantity=cd['update'])
    return redirect(reverse('mavSlice:cart_detail'))


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, product_id=product_id)
    cart.remove(product)
    return redirect(reverse('mavSlice:Cart'))


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'], 'update': True})
    return render(request, 'mavSlice/Cart.html', {'cart': cart})


def product_detail(request, product_id, slug):
    product = get_object_or_404(Product, product_id=product_id, product_slug=slug)
    cart_product_form = CartAddProductForm()
    return render(request, 'mavSlice/product_detail.html',
                  {'product': product, 'cart_product_form': cart_product_form})


def product_list(request):
    products = Product.objects
    print(str(products))


# def signup(request):
#     if not request.user.is_authenticated:
#         if request.method == "POST":
#             form = Registration(request.POST)
#             if form.is_valid():
#                 form.save()
#                 username = form.cleaned_data["username"]
#                 password = form.cleaned_data["password1"]
#                 user = authenticate(username=username, password=password)
#                 login(request, user)
#                 return redirect("mavSlice:home")
#         else:
#             form = Registration()
#         context = {"form": form}
#         return render(request, 'registration/signup.html', context)
#     else:
#         return redirect("mavSlice:home")

# def signup(request):
#     return render(request, 'registration/signup.html',
#                   {'signup': signup})


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('mavSlice:home')
    else:
        form = UserCreationForm()
    return render(request, 'mavSlice/signup.html', {'form': form})


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
                        return redirect("mavSlice:home")
                    else:
                        return redirect("mavSlice:home")
        else:
            form = AuthenticationForm()
        context = {"form": form}
        return render(request, 'registration/login.html', context)
    else:
        return redirect("mavSlice:home")


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect("mavSlice:home")


# Order Functionality
# def order_create(request):
#     cart = Cart(request)
#     if request.method == 'POST':
#         form = OrdersForm(request.POST)
#         if form.is_valid():
#             order = form.save()
#             for product in cart:
#                 OrderProduct.objects.create(order=order, product=product['product'], price=product['price'],
#                                             quantity=product['quantity'])
#             # clear the cart
#             cart.clear()
#             # set the order in the session
#             request.session['order_id'] = order.order_id
#             # redirect for payment
#             return redirect(reverse('mavSlice:process_payment'))
#
#     else:
#         form = OrdersForm()
#     return render(request,
#                   'mavSlice/checkout.html',
#                   {'cart': cart, 'form': form})


@staff_member_required
def admin_order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string('mavSlice/Order/pdf.html',
                            {'order': order})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename=\
        "order_{}.pdf"'.format(order.id)
    weasyprint.HTML(string=html).write_pdf(response,
                                           stylesheets=[weasyprint.CSS(
                                               settings.STATIC_ROOT + 'css/pdf.css')])
    return response


@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request,
                  'admin/admin_order_detail.html',
                  {'order': order})


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'], price=item['price'],
                                         quantity=item['quantity'])
            # clear the cart
            cart.clear()
            # set the order in the session
            request.session['order_id'] = order.order_id

            # Send confirmation email
            subject = 'MavSlice Order Number {} Has Been Placed'.format(order.order_id)
            message = 'Thank you {} for placing an order with MavSlice today.\n' \
                      'In hope to see you again, here is all of our current Coupons:\n{}\n' \
                      'Hope to see you again!'.format(order.first_name, Coupon.objects.all())
            try:
                send_mail(subject, message, 'mavSliceGroup11@gmail.com', [order.email])
                print('Email successfully sent')
            except:
                print('Error: Email not sent')
            # redirect for payment
            return redirect(reverse('mavSlice:process_payment'))

    else:
        form = OrderCreateForm()
    return render(request,
                  'mavSlice/Order/create.html',
                  {'cart': cart, 'form': form})


@login_required
def checkout(request):
    return render(request, 'mavSlice/checkout.html',
                  {'Checkout': checkout})


def payment_process(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, order_id=order_id)

    if request.method == 'POST':
        # retrieve nonce
        nonce = request.POST.get('payment_method_nonce', None)
        # create and submit transaction
        result = braintree.Transaction.sale({
            'amount': '{:.2f}'.format(order.get_total_cost()),
            'payment_method_nonce': nonce,
            'options': {
                'submit_for_settlement': True
            }
        })
        if result.is_success:
            # mark the order as paid
            order.paid = True
            # store the unique transaction id
            order.braintree_id = result.transaction.id
            order.save()
            return redirect('mavSlice:complete_payment')
        else:
            return redirect('mavSlice:payment_canceled')
    else:
        # generate token
        client_token = braintree.ClientToken.generate()
        return render(request, 'mavSlice/payment/process_payment.html', {'order': order, 'client_token': client_token})


def payment_completed(request):
    return render(request, 'mavSlice/payment/payment_complete.html')


def payment_canceled(request):
    return render(request, 'mavSlice/payment/payment_cancelled.html')
