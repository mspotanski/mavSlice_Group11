import uuid
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User, AbstractUser
# 3/15/2022: Unfinished work = determining Product price, storing payment info
# 3/22/2022: Unfinished work = accessing user data, all from 3/15/2022


class Customer(models.Model):
    # We only have to add our extra variables here
    # Current authentication uses username, may need to switch to email
    cust_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='Customer')
    delivery_info = models.OneToOneField('Delivery', null=True, on_delete=models.CASCADE)

    def get_user_email(self):
        return self.user.email

    def get_user_first_name(self):
        return self.user.first_name

    def get_user_last_name(self):
        return self.user.last_name


class Delivery(models.Model):
    # Look at django Address Class, we may be able to get rid of this whole Class
    delivery_id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                                   help_text='Unique ID for this specific order-delivery information')
    user = models.ForeignKey('Delivery', on_delete=models.RESTRICT, null=False)
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


class Product(models.Model):
    # Pizza is our only Product for the store and comes in two types: Whole Pizzas and Slices
    # PRODUCT_TYPES is a dictionary that shows both the type and its related base price
    # Base-price assumes only Cheese Topping
    # There is also only one type of crust if you were curious
    TYPE_SLICE = 'Slice'
    TYPE_WHOLE_PIE = 'Whole Pie'
    SLICE_BASE_PRICE = 3
    WHOLE_PIE_BASE_PRICE = 14
    PRODUCT_TYPES = ((TYPE_SLICE, 'Slice'), (TYPE_WHOLE_PIE, 'Whole Pie'))
    # PRODUCT_PIZZA_NAMES shows all possible flavors of Pizza as well as their number of toppings
    # Toppings determine price (i.e. more toppings = more expensive)
    PRODUCT_PIZZAS = (('Cheese', 0), ('Pepperoni', 1), ('Beef', 1), ('Italian Sausage', 1), ('Canadian Bacon', 1),
                      ('Chicken Alfredo', 2), ('Supreme', 5), ('Meat Lovers', 5), ('Philly', 5), ('BBQ Chicken', 3))
    # PRODUCT_SAUCES is a list of all possible sauces for a pizza
    # Sauce does NOT affect price
    SAUCE_MARINARA = 'Classic Marinara'
    SAUCE_GARLIC_PARM = 'Garlic Parm'
    SAUCE_BUFFALO = 'Buffalo'
    SAUCE_BBQ = 'BBQ'
    SAUCE_NONE = 'None'
    PRODUCT_SAUCES = ((SAUCE_MARINARA, 'Classic Marinara'), (SAUCE_GARLIC_PARM, 'Garlic Parm'),
                      (SAUCE_BUFFALO, 'Buffalo'), (SAUCE_BBQ, 'BBQ'), (SAUCE_NONE, 'None'))
    product_id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for a Product')
    type = models.CharField(max_length=10, choices=PRODUCT_TYPES, blank=False, default='Whole Pie')
    name = models.CharField(max_length=20, choices=PRODUCT_PIZZAS, blank=False, default='Cheese')
    toppings = models.ManyToManyField('Toppings', blank=True, related_name='toppings')
    coupon = models.ManyToManyField('Coupon', blank=True)
    sauce = models.CharField(max_length=16, choices=PRODUCT_SAUCES, blank=False, default='Classic Marinara')
    price = models.DecimalField(blank=False, default=PRODUCT_TYPES, max_digits=6, decimal_places=2)

    def get_price(self):
        return self.price

    def get_type(self):
        return self.type

    # Finds and determines the price of a product based on the product type and number of toppings
    # NOT FINISHED
    # Need to determine proper way to get the number of toppings from the product
    def determine_product_price(self):
        if self.type == 'Slice':
            total = round(3 + (0.30 * len(self.toppings)), 2)
        else:  # self.type == 'Whole Pie'
            total = round(14 + (0.65 * len(self.toppings)), 2)
        return total


class Toppings(models.Model):
    # PRODUCT_TOPPINGS shows all possible toppings for a pizza
    # Each added topping adds 0.30 to slice or 0.65 to whole pizza
    # None indicates a pizza with only Cheese
    # If blank, then default goes to 'None'
    TOP_PEPPERONI = 'Pepperoni'
    TOP_BEEF = 'Beef'
    TOP_SAUSAGE = 'Italian Sausage'
    TOP_CAN_BACON = 'Canadian Bacon'
    TOP_BACON = 'Bacon'
    TOP_CHKN = 'Chicken'
    TOP_GRN_PEPPER = 'Green Pepper'
    TOP_JALEPENO = 'Jalapeno'
    TOP_ONION = 'Onion'
    TOP_BAN_PEPPER = 'Banana Pepper'
    TOP_BLK_OLIVE = 'Black Olive'
    TOP_NONE = 'None'
    PRODUCT_TOPPINGS = ((TOP_PEPPERONI, 'Pepperoni'), (TOP_BEEF, 'Beef'), (TOP_SAUSAGE, 'Italian Sausage'),
                        (TOP_CAN_BACON, 'Canadian Bacon'), (TOP_BACON, 'Bacon'), (TOP_CHKN, 'Chicken'),
                        (TOP_GRN_PEPPER, 'Green Pepper'), (TOP_JALEPENO, 'Jalapeno'), (TOP_ONION, 'Onion'),
                        (TOP_BAN_PEPPER, 'Banana Pepper'), (TOP_BLK_OLIVE, 'Black Olive'), (TOP_NONE, 'None'))
    name = models.CharField(max_length=15, choices=PRODUCT_TOPPINGS, null=False, blank=True, default='None')


class Order(models.Model):
    order_id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for a specific Order')
    # Zero to many relationship from User to Order
    # OneToOne relationship from Order to User
    # customer = models.OneToOneField('Customer', primary_key=True, on_delete=models.CASCADE)
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    payment = models.ForeignKey('Payment', on_delete=models.CASCADE)
    delivery = models.ForeignKey('Delivery', on_delete=models.CASCADE)
    coupon = models.ForeignKey('Coupon', null=True, on_delete=models.CASCADE)
    products = models.ManyToManyField('Product', blank=False)
    order_price = models.DecimalField(blank=False, default=0.00, max_digits=4, decimal_places=2)
    placed_time = models.DateTimeField(default=timezone.now)
    completed_time = models.DateTimeField(default=timezone.now)
    # NOT Finished
    # Need to determine how to grab the price for each individual product
    #
    # def determine_order_price(self.products):
    #     total = 0
    #     for product in products:
    #         total += product.get_price()
    #     return total


class checkout(models.Model):
    pass
