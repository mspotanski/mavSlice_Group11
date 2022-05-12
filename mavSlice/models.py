import uuid
from django.utils import timezone
import braintree
from django.contrib.auth.models import User, AbstractUser
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User


'''
Dealing with no UUID serialization support in json
'''
from json import JSONEncoder
from uuid import UUID
JSONEncoder_olddefault = JSONEncoder.default


def JSONEncoder_newdefault(self, o):
    if isinstance(o, UUID): return str(o)
    return JSONEncoder_olddefault(self, o)


JSONEncoder.default = JSONEncoder_newdefault
# class customer(models.Model):
#     # add additional fields in here
#     # cust_id = models.UUIDField(primary_key=True, default=uuid.uuid4,
#     #                            help_text='Unique ID for this specific order-delivery information')
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     username = models.CharField(max_length=30, null=False)
#     delivery_info = models.ForeignKey('Delivery', on_delete=models.RESTRICT, null=True)
#     first_name = models.CharField(max_length=250, null=False)
#     last_name = models.CharField(max_length=250, null=False)
#     email = models.CharField(max_length=250, null=False)
#     password1 = models.CharField(max_length=250, null=False)
#    # password = models.CharField(max_length=250, null=False)
#     payment_info = models.CharField(max_length=250, null=True)

# @receiver(post_save, sender=User)
# def update_user_customer(sender, instance, created, **kwargs):
#     if created:
#         customer.objects.create(user=instance)
#     instance.customer.save()
#
# @receiver(post_save, sender=User)
# def create_customer(sender, instance, created, **kwargs):
#     if created:
#         customer.objects.create(user=instance)
#
# @receiver(post_save, sender=User)
# def save_customer(sender, instance, **kwargs):
#     instance.customer.save()
#
#     def __str__(self):
#          return self.email


# DELIVERY_CITIES = [('OMA', 'Omaha'), ('BNGTN', 'Bennington'), ('PAP', 'Papillion'), ('GTNA', 'Gretna'),
#                    ('ELK', 'Elkhorn'), ('BEN', 'Benson'), ('RAL', 'Ralston'), ('CB', 'Council Bluffs')]

#DELIVERY_STATES = [('NE', 'Nebraska'), ('IA', 'Iowa')]


# class Delivery(models.Model):
#     # Look at django Address Class, we may be able to get rid of this whole Class
#     delivery_id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this specific order')
#     street_address = models.CharField(max_length=250, null=False)
#     street_address2 = models.CharField(max_length=250, null=True, blank=True, default='NA',
#                                        help_text='Apt number, building, etc.')
#     # Note that for this project, our store will only be in Omaha, so these fields could be eliminated theoretically
#     city = models.CharField(max_length=30, null=False)
#     state = models.CharField(max_length=30, null=False, choices=DELIVERY_STATES, default='NE')
#     zipCode = models.CharField(max_length=5, null=False)
#
#     def get_delivery_info(self):
#         return [self.street_address, self.street_address2, self.city, self.state, self.zipCode]
#
#     def __str__(self):
#         return '{} () {}, {} {}'.format(self.street_address, self.street_address2, self.city, self.state, self.zipCode)


# NOT FINISHED
# class Payment(models.Model):
#     # Look at django Address Class, they have a whole form for payment information
#     # Look at Brain Tree for implementation
#     pay_id = models.UUIDField(primary_key=True, default=uuid.uuid4,
#                               help_text='Unique ID for User Billing Info')


class Coupon(models.Model):
    coupon_id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                                 help_text='Unique ID for given Coupon and its discount')
    totalDiscount = models.DecimalField(blank=True, default=0.00, decimal_places=2, max_digits=5)
    name = models.CharField(blank=True, default='NA', max_length=25)

    def __str__(self):
        return '{name}: {discount}'.format(name=self.name, discount=self.totalDiscount)


class Product(models.Model):
    # Pizza is our only Product for the store and comes in two types: Whole Pizzas and Slices
    # PRODUCT_TYPES is a dictionary that shows both the type and its related base price
    # Base-price assumes only Cheese Topping
    # There is also only one type of crust if you were curious
    TYPE_SLICE = 'Slice'
    TYPE_WHOLE_PIE = 'Whole Pie'
    # SLICE_BASE_PRICE = 3
    # WHOLE_PIE_BASE_PRICE = 14
    PRODUCT_TYPES = ((TYPE_SLICE, 'Slice'), (TYPE_WHOLE_PIE, 'Whole Pie'))
    # PRODUCT_PIZZA_NAMES shows all possible flavors of Pizza as well as their number of toppings
    PRODUCT_PIZZAS = (('CHS', 'Cheese'), ('PEPP', 'Pepperoni'), ('BF', 'Beef'),
                      ('MAC', 'Macaroni and Cheese'), ('VG', 'Veggie'),
                      ('BFF', 'Buffalo '), ('SPRM', 'Supreme'), ('MRG', 'Margherita'),
                      ('HWI', 'Hawaiian'), ('BBQ_CHKN', 'BBQ Chicken'))

    # PRODUCT_SAUCES is a list of all possible sauces for a pizza
    # Sauce does NOT affect price
    PRODUCT_SAUCES = (('MARINARA', 'Classic Marinara'), ('G_PARM', 'Garlic Parm'),
                      ('BUF', 'Buffalo'), ('BBQ', 'Barbecue'), ('NA', 'None'))

    # Toppings determine price (i.e. more toppings = more expensive)
    # Topping price if Product.Type == Slice = 0.30
    # Topping price if Product.Type == Whole = 0.60
    PRODUCT_TOPPINGS = (('TOP_PEPP', 'Pepperoni'), ('TOP_BF', 'Beef'), ('TOP_SAUS', 'Italian Sausage'),
                        ('TOP_CA_BAC', 'Canadian Bacon'), ('TOP_BAC', 'Bacon'), ('TOP_CHKN', 'Chicken'),
                        ('TOP_GRN_PEP', 'Green Pepper'), ('TOP_JAL', 'Jalapeno'), ('TOP_ONION', 'Onion'),
                        ('TOP_BAN_PEP', 'Banana Pepper'), ('TOP_BLK_OLV', 'Black Olive'), ('TOP_NONE', 'None'))

    product_id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for a Product')
    type = models.CharField(max_length=10, choices=PRODUCT_TYPES, blank=False, default='Whole Pie')
    name = models.CharField(max_length=20, choices=PRODUCT_PIZZAS, blank=False, default='Cheese')
    has_toppings = models.BooleanField
    has_sauce = models.BooleanField
    description = models.CharField(max_length=1000, blank=True)
    coupon = models.ManyToManyField('Coupon', blank=True)
    sauce = models.CharField(max_length=16, choices=PRODUCT_SAUCES, blank=False, default='Classic Marinara')
    price = models.DecimalField(blank=False, default=PRODUCT_TYPES, max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='images/', blank=True)
    product_slug = models.SlugField(max_length=100, db_index=True)

    class Meta:
        ordering = ('product_id',)
        index_together = (('product_id', 'product_slug'),)

    def get_price(self):
        return self.price

    def get_type(self):
        return self.type

    def set_price(self, value):
        if value >= 0:
            self.price = value

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('mavSlice:product_detail', args=[self.product_id, self.product_slug])


# Subtype of Product
# Should inherit all variables and methods of Product
# Purpose is to make it easier to store and determine prices of custom pizzas
class customProduct(Product):
    has_extra_cheese = models.BooleanField
    has_extra_toppings = models.BooleanField

    def __str__(self):
        return 'Sauce: {sauce}\nToppings: {tops}\t\tExtra Toppings:{extra_top}\nExtra Cheese: {is_cheese}\n'.format(
            sauce=self.sauce, tops=self.description, extra_top=self.has_extra_toppings, is_cheese=self.has_extra_cheese)


class Order(models.Model):
    order_id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for a specific Order')
    # Zero to many relationship from User to Order
    # OneToOne relationship from Order to User
    #customer = models.OneToOneField('customer', on_delete=models.CASCADE, help_text='User who placed order')
    # User = models.ForeignKey('User', on_delete=models.CASCADE)
    #payment = models.ForeignKey('Payment', on_delete=models.CASCADE)
    #delivery = models.ForeignKey('Delivery', on_delete=models.CASCADE)
    #coupon = models.ForeignKey('Coupon', null=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=250, default='')
    zip = models.CharField(max_length=20, default='')
    state = models.CharField(max_length=20, default='')
    city = models.CharField(max_length=100, default='')
    order_price = models.DecimalField(blank=False, default=0.00, max_digits=4, decimal_places=2)
    placed_time = models.DateTimeField(default=timezone.now)
    completed_time = models.DateTimeField(default=timezone.now)
    braintree_id = models.CharField(max_length=150, blank=True)
    is_completed = models.BooleanField(default=False)

    def set_order_price(self):
        temp = 0
        items = OrderItem.objects.filter(order__order_id__exact=self.order_id)
        for item in items:
            temp += item.get_cost()
        self.order_price = temp
#
#     class Meta:
#         ordering = ('-placed_time',)
#
#     def __str__(self):
#         return 'Order {}'.format(self.id)
#
#     def get_total_cost(self):
#         return sum(item.get_cost() for item in self.items.all())
#     # def determine_order_price(self):
#     #     total = 0
#     #     for product in Product.objects.filter():
#     #         total += product.get_price()
#     #     return total
#
#
# # Resolves Many-to-Many relationship between Order and Product
# class OrderProduct(models.Model):
#     order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     quantity = models.PositiveIntegerField(default=1)
#
#
#     def __str__(self):
#         return '{}'.format(self.id)
#
#     def get_cost(self):
#         return self.price * self.quantity
#
    class Meta:
        ordering = ('placed_time',)

    def __str__(self):
        return 'Order {}:\nPlaced Time: {}\nOrder Items:{}\n'.format(self.order_id, self.placed_time,
                                                                     OrderItem.objects.filter(
                                                                         order_id__exact=self.order_id))

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.order.order_id)

    def get_cost(self):
        return self.price * self.quantity