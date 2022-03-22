from django.contrib import admin
from .models import *
# 3/22/2022 Unfinished work: accessing user data from customer for CustomerList


# Define the admin options for the Customer table
# Should be able to see name, email, Delivery information, user_id
# Delivery info includes: address,
class CustomerList(admin.ModelAdmin):
    list_display = ('cust_id', 'user.email', 'user.first_name', 'user.last_name', 'delivery_info.street_address',
                    'delivery_info.street_address2', 'delivery_info.city', 'delivery_info.state',
                    'delivery_info.zipCode')
    list_filter = ('user.last_name', 'cust_id',)
    search_fields = ('cust_id', 'user.first_name', 'user.last_name', 'user.email', 'delivery_info.zipCode')
    ordering = ['user.last_name', 'cust_id']


# Define the admin options for the Order table
# Should be able to display Order ID,
class OrderList(admin.ModelAdmin):
    list_display = ('order_id', 'products', 'customer', 'coupon', 'order_price', 'placed_time', 'completed_time')
    list_filter = ('placed_time', 'customer', 'order_id')
    search_fields = ('customer', 'order_id', 'products', 'coupon', 'placed_time', 'completed_time')
    ordering = ['placed_time', 'customer', 'order_id']


# Define the admin options for the Product table
# Same thing as Menu, but in a List format for admin
class ProductList(admin.ModelAdmin):
    list_display = ('product_id', 'name', 'type', 'price')
    list_filter = ('type', 'name')
    search_fields = ('name', 'product_id')
    ordering = ['name', 'product_id']


class ToppingsList(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)
    search_fields = ('name', )
    ordering = ['name']


# register the Service and Product with the django admin page
admin.site.register(Customer, CustomerList)
admin.site.register(Order, OrderList)
admin.site.register(Product, ProductList)
admin.site.register(Toppings, ToppingsList)
