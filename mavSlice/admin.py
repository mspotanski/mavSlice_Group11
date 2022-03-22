from django.contrib import admin
from .models import *


# Define the admin options for the Customer table
# Should be able to see name, email, Delivery information, user_id
# Delivery info includes: address,
class CustomerList(admin.ModelAdmin):
    list_display = ('cust_name', 'phone')
    list_filter = ('cust_name',)
    search_fields = ('cust_name', )
    ordering = ['cust_name']


# Define the admin options for the Order table
# Should be able to display Order ID,
class OrderList(admin.ModelAdmin):
    list_display = ('cust_name',)
    list_filter = ('cust_name',)
    search_fields = ('cust_name',)
    ordering = ['cust_name']


# Define the admin options for the Product table
# Same thing as Menu, but in a List format for admin
class ProductList(admin.ModelAdmin):
    list_display = ('product',)
    list_filter = ('cust_name',)
    search_fields = ('product', 'cust_name')
    ordering = ['cust_name']


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
