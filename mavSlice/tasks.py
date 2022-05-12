from django.core.mail import send_mail
from celery import *
from models import *


@task
def order_created(input_order_id):
    """
    Task to send an e-mail notification when an order is
    successfully created.
    """
    order = Order.objects.get(order_id=input_order_id)
    subject = 'Order nr. {}'.format(order.order_id)
    message = 'Dear {},\n\nYou have successfully placed an order.\
                  Your order id is {}.'.format(order.first_name, order.order_id)
    mail_sent = send_mail(subject, message, 'mavSliceGroup11@gmail.com', [order.email])
    return mail_sent


@task
# Sends newly registered user list of coupon codes to use at checkout
# NOT DONE: LEAVE FOR SPRINT 3
def account_registered(cust_id):
    pass

