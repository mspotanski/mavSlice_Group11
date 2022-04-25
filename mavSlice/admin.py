from django.contrib import admin
from .models import *
from django.urls import reverse
from django.utils.safestring import mark_safe
# Define the admin options for the Customer table
# Should be able to see name, email, Delivery information, user_id


#Delivery info includes: address,
# class CustomerList(admin.ModelAdmin):
#     list_display = ('email', 'first_name', 'last_name')
#     #list_display = ('cust_id', 'user.email', 'user.first_name', 'user.last_name', 'delivery_info.street_address',
#     #                'delivery_info.street_address2', 'delivery_info.city', 'delivery_info.state',
#     #                'delivery_info.zipCode')
#     #list_filter = ('user.last_name', 'cust_id',)
#     list_filter = ('email', 'last_name')
#     search_fields = ('email', 'last_name')
#     # ordering = ['user.last_name', 'cust_id']
#     ordering = ['email']
#
# class DeliveryList(admin.ModelAdmin):
#     list_display = ('street_address', 'street_address2', 'city', 'state', 'zipCode',)
#     #list_filter = ('customer',)
#     search_fields = ('state', 'city', 'street_address', 'street_address2', 'zipCode',)
#     ordering = ['zipCode']
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


# class OrderItemInline(admin.TabularInline):
#     model = OrderProduct
#     raw_id_fields = ['product']


# def order_detail(obj):
#     return mark_safe('<a href="{}">View</a>'.format(
#         reverse('mavSlice:admin_order_detail', args=[obj.id])))


# @admin.register(Order)
# class OrderAdmin(admin.ModelAdmin):
#     list_display = ['order_id', 'order_price', 'placed_time', 'coupon', 'delivery', order_detail]
#     list_filter = ['order_price', 'placed_time', 'coupon']
#     inlines = [OrderItemInline]


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
#admin.site.register(customer, CustomerList)
#admin.site.register(Order, OrderList)
admin.site.register(Product, ProductList)
#admin.site.register(Delivery, DeliveryList)
admin.site.register(Coupon, CouponList)


def order_detail(obj):
    return mark_safe('<a href="{}">View</a>'.format(
        reverse('orders:admin_order_detail', args=[obj.id])))


def export_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment;' \
                                      'filename={}.csv'.format(opts.verbose_name)
    writer = csv.writer(response)

    fields = [field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many]
    # Write a first row with header information
    writer.writerow([field.verbose_name for field in fields])
    # Write data rows
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)
    return response


export_to_csv.short_description = 'Export to CSV'


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


def order_pdf(obj):
    return mark_safe('<a href="{}">PDF</a>'.format(
        reverse('orders:admin_order_pdf', args=[obj.id])))


order_pdf.short_description = 'Invoice'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [ 'first_name', 'last_name', 'email',
                    'address', 'zip', 'city',
                     order_detail, order_pdf]
    #list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]
    actions = [export_to_csv]