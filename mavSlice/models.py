import uuid
from django.db import models
from django.utils import timezone
import decimal
from django.contrib.auth.models import User, AbstractUser

# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # add additional fields in here
    delivery_info = customer = models.ForeignKey('Delivery', on_delete=models.RESTRICT, null=True)

    def __str__(self):
        return self.email


class Delivery(models.Model):
    # Look at django Address Class, we may be able to get rid of this whole Class
    delivery_id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                                   help_text='Unique ID for this specific order-delivery information')
    street_address = models.CharField(max_length=250, null=False)
    street_address2 = models.CharField(max_length=250, null=True, blank=True, help_text='Apt number, building, etc.')
    # Note that for this project, our store will only be in Omaha, so these fields could be eliminated theoretically
    city = models.CharField(max_length=30, null=False)
    state = models.CharField(max_length=30, null=False)
    zipCode = models.CharField(max_length=5, null=False)


# NOT FINISHED
class Payment(models.Model):
    # Look at django Address Class, they have a whole form for payment information
    pay_id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                              help_text='Unique ID for User Billing Info')


class Coupon(models.Model):
    coupon_id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                                 help_text='Unique ID for given Coupon and its discount')
    totalDiscount = models.DecimalField(blank=True, default=0.00, decimal_places=2, max_digits=5)
    name = models.CharField(blank=True, default='NA')

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
                      ('ITL_SAUS', 'Italian Sausage'), ('CA_BAC', 'Canadian Bacon'),
                      ('CHKN_ALF', 'Chicken Alfredo'), ('SPRM', 'Supreme'), ('MT_LOVE', 'Meat Lovers'),
                      ('PHIL', 'Philly'), ('BBQ_CHKN', 'BBQ Chicken'))

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
    description = models.CharField(max_length=1000, blank=True)
    has_toppings = models.BooleanField
    has_extra_cheese = models.BooleanField
    has_extra_toppings = models.BooleanField
    has_sauce = models.BooleanField
    coupon = models.ManyToManyField('Coupon', blank=True)
    # sauce = models.CharField(max_length=16, choices=PRODUCT_SAUCES, blank=False, default='Classic Marinara')
    price = models.DecimalField(blank=False, default=PRODUCT_TYPES, max_digits=6, decimal_places=2)

    def get_price(self):
        return self.price

    def get_type(self):
        return self.type

    def set_price(self, value):
        if value >= 0:
            self.price = value

    def __str__(self):
        return self.description

    # Finds and determines the price of a product based on the product type and number of toppings
    # NOT FINISHED
    # Need to determine proper way to get the number of toppings from the product
    # def determine_product_price(self):
    #     if self.type == 'Slice':
    #         total = round(3 + (0.30 * len(self.toppings)), 2)
    #     else:  # self.type == 'Whole Pie'
    #         total = round(14 + (0.65 * len(self.toppings)), 2)
    #     return total


# class Toppings(models.Model):
#     # PRODUCT_TOPPINGS shows all possible toppings for a pizza
#     # Each added topping adds 0.30 to slice or 0.65 to whole pizza
#     # None indicates a pizza with only Cheese
#     # If blank, then default goes to 'None'
#     PRODUCT_TOPPINGS = (('TOP_PEPP', 'Pepperoni'), ('TOP_BF', 'Beef'), ('TOP_SAUS', 'Italian Sausage'),
#                         ('TOP_CA_BAC', 'Canadian Bacon'), ('TOP_BAC', 'Bacon'), ('TOP_CHKN', 'Chicken'),
#                         ('TOP_GRN_PEP', 'Green Pepper'), ('TOP_JAL', 'Jalapeno'), ('TOP_ONION', 'Onion'),
#                         ('TOP_BAN_PEP', 'Banana Pepper'), ('TOP_BLK_OLV', 'Black Olive'), ('TOP_NONE', 'None'))
#     name = models.CharField(max_length=15, choices=PRODUCT_TOPPINGS, null=False, blank=True, default='None')


class Order(models.Model):
    order_id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for a specific Order')
    # Zero to many relationship from User to Order
    # OneToOne relationship from Order to User
    # customer = models.OneToOneField('Customer', primary_key=True, on_delete=models.CASCADE)
    customer = models.ForeignKey('User', on_delete=models.CASCADE)
    payment = models.ForeignKey('Payment', on_delete=models.CASCADE)
    delivery = models.ForeignKey('Delivery', on_delete=models.CASCADE)
    coupon = models.ForeignKey('Coupon', null=True, on_delete=models.CASCADE)
    products = models.ManyToManyField('Product', blank=False)
    order_price = models.DecimalField(blank=False, default=0.00, max_digits=4, decimal_places=2)
    placed_time = models.DateTimeField(default=timezone.now)
    completed_time = models.DateTimeField(default=timezone.now)
    # NOT Finished
    # Need to determine how to grab the price for each individual product

    # def determine_order_price(self):
    #     total = 0
    #     for product in Product.objects.filter():
    #         total += product.get_price()
    #     return total
