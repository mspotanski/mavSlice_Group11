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
from .views import register_view, login_view, logout_view
from django.urls import path, re_path
from .views import HomePageView
app_name = 'mavSlice'
urlpatterns = [
    path('', views.home, name='home'),
    re_path(r'^home/$', views.home, name='home'),
    path('', HomePageView.as_view(), name='home'),
    path('Menu/', views.Menu, name='Menu'),
    path('Cart/', views.Cart, name='Cart'),
    path('custom/', views.custom, name='custom'),
    path('Cart/delivery/', views.cart_delivery, name='cart_delivery'),
    path('Cart/delivery/order_confirmation/', views.order_confirmation, name='order_confirmation'),
    path('checkout/', views.checkout, name='checkout'),
    path('coupon/create/', views.coupon_new, name='coupon_new'),
    path('coupon/<int:pk>/edit/', views.coupon_edit, name='coupon_edit'),
    path('coupon/list/', views.coupon_list, name='coupon_list'),
    path('customer/list/', views.customer_list, name='customer_list'),
    path('product/<int:pk>/delete/', views.product_delete, name='product_delete'),
    path('user/<int:pk>/summary/', views.user_info, name='user_info'),
    path('user/<int:pk>/summary/delivery/', views.user_info_delivery, name='user_info_delivery'),
    path('user/<int:pk>/summary/payment/', views.user_info_payment, name='user_info_payment'),

]
