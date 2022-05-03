from django.contrib import admin
from .models import *
from django.urls import reverse
from django.utils.safestring import mark_safe


# Define the admin options for the Customer table
# Should be able to see name, email, Delivery information, user_id


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


def order_detail(obj):
    return mark_safe('<a href="{}">View</a>'.format(
        reverse('mavSlice:admin_order_detail', args=[obj.order_id])))


#
# def export_to_csv(modeladmin, request, queryset):
#     opts = modeladmin.model._meta
#     response = HttpResponse(content_type='text/csv')
#     response['Content-Disposition'] = 'attachment;' \
#                                       'filename={}.csv'.format(opts.verbose_name)
#     writer = csv.writer(response)
#
#     fields = [field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many]
#     # Write a first row with header information
#     writer.writerow([field.verbose_name for field in fields])
#     # Write data rows
#     for obj in queryset:
#         data_row = []
#         for field in fields:
#             value = getattr(obj, field.name)
#             if isinstance(value, datetime.datetime):
#                 value = value.strftime('%d/%m/%Y')
#             data_row.append(value)
#         writer.writerow(data_row)
#     return response
#
#
# export_to_csv.short_description = 'Export to CSV'


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


def order_pdf(obj):
    return mark_safe('<a href="{}">PDF</a>'.format(
        reverse('mavSlice:admin_order_pdf', args=[obj.order_id])))


order_pdf.short_description = 'Invoice'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'address', 'zip', 'city',
                    order_detail, order_pdf]
    # list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]
    # actions = [export_to_csv]


# register the Service and Product with the django admin page
# admin.site.register(customer, CustomerList)
# admin.site.register(Order, OrderList)
admin.site.register(Product, ProductList)
admin.site.register(Coupon, CouponList)
