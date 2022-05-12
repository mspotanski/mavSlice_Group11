"""djangoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views. Home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.conf.urls import url
from . import views
from django.urls import path, re_path
from django.conf.urls.static import static
from django.conf import settings

# from django.conf.urls import url
# from mysite.core import views as core_views

app_name = 'mavSlice'

urlpatterns = [
    path('', views.home, name='home'),
    re_path(r'^home/$', views.home, name='home'),
    re_path(r'^Cart/$', views.cart_detail, name='Cart'),
    path('Menu/WholePies/', views.Menu, name='Menu'),
    path('Menu/Slice/', views.slice_Menu, name='slice_Menu'),
    path('Cart/', views.cart_detail, name='cart_detail'),
    path('add/<str:product_id>/', views.cart_add, name='cart_add'),
    path('remove/<str:product_id>/', views.cart_remove, name='cart_remove'),
    path('custom/', views.custom, name='custom'),
    path('signup/', views.signup, name='signup'),
    path('Cart/order_confirmation/', views.payment_completed, name='order_confirmation'),
    path('checkout/', views.checkout, name='checkout'),
    # path('user/<int:pk>/summary/', views.user_info, name='user_info'),
    # path('user/<int:pk>/summary/delivery/', views.user_info_delivery, name='user_info_delivery'),
    # path('user/<int:pk>/summary/payment/', views.user_info_payment, name='user_info_payment'),
    path('place_order/', views.order_create, name='order_create'),
    path('admin/order/<str:order_id>/', views.admin_order_detail, name='admin_order_detail'),
    path('Menu/<str:product_id>/<slug:slug>/', views.product_detail, name='product_detail'),
    path('create/payment/process/', views.payment_process, name='process_payment'),
    path('complete/', views.payment_completed, name='complete_payment'),
    path('canceled/', views.payment_canceled, name='payment_canceled'),
    path('create/', views.order_create, name='order_create'),
    path('admin/order/<str:order_id>/', views.admin_order_detail, name='admin_order_detail'),
    path('admin/order/<str:order_id>/pdf/', views.admin_order_pdf, name='admin_order_pdf'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
