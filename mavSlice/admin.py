from django.contrib import admin
from .models import *
from django.urls import reverse
from django.utils.safestring import mark_safe
# Define the admin options for the Customer table
# Should be able to see name, email, Delivery information, user_id


#Delivery info includes: address,
class CustomerList(admin.ModelAdmin):
    list_display = ('email', 'cust_fname', 'cust_lname')
    #list_display = ('cust_id', 'user.email', 'user.first_name', 'user.last_name', 'delivery_info.street_address',
    #                'delivery_info.street_address2', 'delivery_info.city', 'delivery_info.state',
    #                'delivery_info.zipCode')
    #list_filter = ('user.last_name', 'cust_id',)
    list_filter = ('email', 'cust_lname')
    search_fields = ('email', 'cust_lname')
    # ordering = ['user.last_name', 'cust_id']
    ordering = ['email']


class DeliveryList(admin.ModelAdmin):
    list_display = ('street_address', 'street_address2', 'city', 'state', 'zipCode',)
    #list_filter = ('customer',)
    search_fields = ('state', 'city', 'street_address', 'street_address2', 'zipCode',)
    ordering = ['zipCode']


# Define the admin options for the Order table
# Should be able to display Order ID,
# @admin.register(Order)
# class OrderList(admin.ModelAdmin):
#     list_display = ('order_id', 'coupon', 'order_price', 'placed_time', 'completed_time')
#     # list_display = ('order_id', 'products', 'customer', 'coupon', 'order_price', 'placed_time', 'completed_time')
#     list_filter = ('order_id', 'placed_time', 'completed_time')
#     # list_filter = ('placed_time', 'user', 'order_id')
#     inlines = [OrderItemInline]
#     search_fields = ('order_id', 'products', 'coupon', 'placed_time', 'completed_time')
#     ordering = ['placed_time', 'order_id']


class OrderItemInline(admin.TabularInline):
    model = OrderProduct
    raw_id_fields = ['product']


def order_detail(obj):
    return mark_safe('<a href="{}">View</a>'.format(
        reverse('mavSlice:admin_order_detail', args=[obj.id])))


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'order_price', 'placed_time', 'coupon', 'delivery', order_detail]
    list_filter = ['order_price', 'placed_time', 'coupon']
    inlines = [OrderItemInline]


# Define the admin options for the Product table
# Same thing as Menu, but in a List format for admin
class ProductList(admin.ModelAdmin):
    list_display = ('product_id', 'product_slug', 'name', 'type', 'price')
    list_filter = ('type', 'name')
    search_fields = ('name', 'product_id')
    ordering = ['name', 'product_id']
    prepopulated_fields = {'product_slug': ('name',)}


class CouponList(admin.ModelAdmin):
    list_display = ('coupon_id', 'name', 'totalDiscount')
    list_filter = ('name', 'totalDiscount')
    search_fields = ('name', 'coupon_id', 'totalDiscount')
    ordering = ['name', 'totalDiscount']


# register the Service and Product with the django admin page
admin.site.register(customer, CustomerList)
#admin.site.register(Order, OrderList)
admin.site.register(Product, ProductList)
admin.site.register(Delivery, DeliveryList)
admin.site.register(Coupon, CouponList)
