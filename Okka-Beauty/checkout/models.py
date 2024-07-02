from django.db import models
from user.models import *
from product.models import *
from django.conf import settings 

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.core.mail import EmailMultiAlternatives
from django.urls import reverse

from decimal import Decimal


# Create your models here.
class Address(models.Model):
    ADDRESS_TYPE_CHOICES = [
        ('Billing', 'Billing'),
        ('Shipping', 'Shipping'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    company = models.CharField(max_length=100, blank=True, null=True)
    address_1 = models.CharField(max_length=255)
    address_2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    postcode = models.CharField(max_length=20)
    Country_Region = models.CharField(max_length=100)
    state_country = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address_type = models.CharField(max_length=20, choices=ADDRESS_TYPE_CHOICES)

    def __str__(self):
        return f"{self.address_type} Address for {self.user.username}"

class Order(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('card', 'Credit Card'),
    ]
    PAYMENT_STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('paid', 'Paid'),
        ('decline', 'Decline'),
        ('canceled', 'Canceled'),
    )
    ORDER_STATUS_CHOICES = [
        ('on-hold', 'On-Hold'),
        ('processing', 'Processing'),
        ('Confirmed', 'Confirmed'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_id = models.CharField(max_length=100, unique=True)
    products = models.ManyToManyField(Product, through='OrderItem')
    billing_address = models.ForeignKey(Address, related_name='billing_address', on_delete=models.CASCADE)
    shipping_address = models.ForeignKey(Address, related_name='shipping_address', on_delete=models.CASCADE)
    currency = models.CharField(max_length=20, default="AED")
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=Decimal('0.00'))
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=Decimal('0.00'))
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=Decimal('0.00'))
    disc_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=Decimal('0.00'))
    bill_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=Decimal('0.00'))
    payment_method = models.CharField(max_length=100, choices=PAYMENT_METHOD_CHOICES)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='Pending')
    order_status = models.CharField(max_length=100, choices=ORDER_STATUS_CHOICES, default='pending')
    order_date = models.DateField()
    order_confirmation_date = models.DateField(blank=True, null=True)
    shipment_date = models.DateField(blank=True, null=True)
    delivery_date = models.DateField(blank=True, null=True)
    cancel_date = models.DateField(blank=True, null=True)
    cancel_status = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    order_processed = models.BooleanField(default=False)
    order_notes = models.TextField(blank=True)
    track_id = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Order ID: {self.order_id}"

    def save(self, *args, **kwargs):
        print("Before save - Order Status:", self.order_status)

        if self.order_status == 'Confirmed' and not self.order_confirmation_date:
            self.order_confirmation_date = timezone.now()
        elif self.order_status == 'Shipped' and not self.shipment_date:
            self.shipment_date = timezone.now()
        elif self.order_status == 'Delivered':
            if not self.delivery_date:
                self.delivery_date = timezone.now()
            self.payment_status = 'paid'
        elif self.order_status == 'Cancelled' and not self.cancel_date:
            self.cancel_date = timezone.now()

        print("After save - Order Status:", self.order_status)
        print("Order Confirmation Date:", self.order_confirmation_date)
        print("Shipment Date:", self.shipment_date)
        print("Delivery Date:", self.delivery_date)
        print("Cancel Date:", self.cancel_date)

        if not self.order_id:
            last_order = Order.objects.order_by('-order_id').first()
            if last_order:
                # Extract the numeric part of the order_id by slicing off the first four characters
                last_order_id = int(last_order.order_id[4:])  # Extract numeric part of order_id
                new_order_id = 'Okka' + str(last_order_id + 1).zfill(6)
            else:
                new_order_id = 'Okka000001'
            self.order_id = new_order_id


            print(self.order_id)

        if not self.order_date:
            self.order_date = timezone.now().date()

        previous_status = ''
        try:
            previous_status = str(self.__class__.objects.get(pk=self.pk).order_status).strip()
            print(previous_status)
        except self.__class__.DoesNotExist:
            pass

        if self.order_status and self.order_status == 'Delivered' and not self.delivery_date:
            self.delivery_date = timezone.now()
            print(self.delivery_date)

        super().save(*args, **kwargs)


        current_status = str(self.order_status).strip()

        print("Previous Status:", previous_status)
        print("Current Status:", current_status)

        if previous_status.lower() == 'processing' and current_status.lower() == 'confirmed':
            print('Order confirmed')
            # Send order shipped email
            item_count = OrderItem.objects.filter(order_id=self.id).count()
            print(item_count)
            invoice_id = Invoice.objects.values_list('invoice_id', flat=True).get(order=self.id)
            print(invoice_id)
            email_subject = 'Your Alsuwaidi in  Order #{} of {} item'.format(self.order_id, item_count) 

            # current_site = get_current_site(kwargs.get('request'))
            # site_url = f"http://{current_site.domain}"
            # print(site_url)
            
            # track_url = reverse('order_tracking', kwargs={'order_id': self.order_id})
            # invoice_url = reverse('download_invoice', kwargs={'order_id': self.id,'invoice_id': invoice_id})
            # order_url = reverse('order_sucess',  kwargs={'order_id': self.id})

            # order_track = f"https://suwaidionline.com{track_url}"
            # order_invoice = f"https://suwaidionline.com{invoice_url}"
            # order_page = f"https://suwaidionline.com/{order_url}"

            # print(order_track)
            # print(order_invoice)
            email_body = render_to_string('email/order/order_confirm.html', {
                'order': self,
                'order_item': OrderItem.objects.filter(order_id=self.id),
                'user': self.user,
                'order_id': self.order_id,
                'shippingaddress': Address.objects.get(id=self.shipping_address.id),
                'billingaddress': Address.objects.get(id=self.billing_address.id),
                'payment': self.payment_method,
                'iteam_total': self.amount,
                'tax': self.tax_amount,
                'disc_price': self.disc_price,
                'total': self.bill_amount,
                'order_date': self.order_date,
                # 'site_url': site_url,
                # 'order_track': order_track,
                # 'order_invoice': order_invoice,
                # 'order_page':order_page,
            })
            safe_email_body = mark_safe(email_body)
            email = EmailMultiAlternatives(
                email_subject, 
                body=safe_email_body, 
                from_email='settings.ADMIN_EMAIL', 
                to=[self.user.email],
            )   
            email.attach_alternative(safe_email_body, "text/html")

            #Send email to admin
            admin_email = settings.ADMIN_EMAIL
            cc_email = settings.CC_EMAIL
            # admin_subject = 'New Order Received'
            admin_subject = f"New order received from {self.user}. Order ID: {self.order_id}"
                
            admin_email_body = render_to_string('email/order/order_confirm.html', {
				'order': self,
				'order_item': OrderItem.objects.filter(order_id=self.id),
				'user': self.user,
				'order_id': self.order_id,
				'shippingaddress': Address.objects.get(id=self.shipping_address.id),
				'billingaddress': Address.objects.get(id=self.billing_address.id),
				'payment': self.payment_method,
				'iteam_total': self.amount,
				'tax': self.tax_amount,
				'disc_price': self.disc_price,
				'total': self.bill_amount,
				'order_date': self.order_date,
				# 'site_url': site_url,
				# 'order_track': order_track,
				# 'order_invoice': order_invoice,
				# 'order_page':order_page,
            })
            safe_admin_email_body = mark_safe(admin_email_body)
            admin_email = EmailMultiAlternatives(
                admin_subject,
                safe_admin_email_body,
                from_email='settings.ADMIN_EMAIL',
                to=[admin_email],
                cc=cc_email,
            )
            admin_email.attach_alternative(safe_admin_email_body, "text/html")
            admin_email.send()


            email.send()
            print("email send to user and Admin")
            
        elif previous_status.lower() == 'confirmed' and current_status.lower() == 'shipped':
            print('Order Shipped')
            # Send order shipped email
            item_count = OrderItem.objects.filter(order_id=self.id).count()
            print(item_count)
            invoice_id = Invoice.objects.values_list('invoice_id', flat=True).get(order=self.id)
            print(invoice_id)


            # delivery_person = OrderDeliveryPerson.objects.get(order=self.id)
            


            email_subject = 'Your Alsuwaidi in  Order #{} of {} item has been dispatched'.format(self.order_id, item_count) 

            # current_site = get_current_site(kwargs.get('request'))
            # site_url = f"http://{current_site.domain}"
            # print(site_url)
            
            # track_url = reverse('order_tracking', kwargs={'order_id': self.order_id})
            # invoice_url = reverse('download_invoice', kwargs={'order_id': self.id,'invoice_id': invoice_id})
            # order_url = reverse('order_sucess',  kwargs={'order_id': self.order_id})

            # order_track = f"https://suwaidionline.com{track_url}"
            # order_invoice = f"https://suwaidionline.com{invoice_url}"
            # order_page = f"https://suwaidionline.com{order_url}"

            # print(order_track)
            # print(order_invoice)
            email_body = render_to_string('email/order/order_shipped.html', {
                'order': self,
                'order_item': OrderItem.objects.filter(order_id=self.id),
                'user': self.user,
                'order_id': self.order_id,
                'shippingaddress': Address.objects.get(id=self.shipping_address.id),
                'billingaddress': Address.objects.get(id=self.billing_address.id),
                'payment': self.payment_method,
                'iteam_total': self.amount,
                'tax': self.tax_amount,
                'disc_price': self.disc_price,
                'total': self.bill_amount,
                'order_date': self.order_date,
                # 'site_url': site_url,
                # 'order_track': order_track,
                # 'order_invoice': order_invoice,
                # 'order_page':order_page,
                # 'delivery_person_details': delivery_person,
            })
            safe_email_body = mark_safe(email_body)
            email = EmailMultiAlternatives(
                email_subject,
                body=safe_email_body,
                from_email= settings.ADMIN_EMAIL,
                to=[self.user.email],
            )
            email.attach_alternative(safe_email_body, "text/html")
            email.send()
            print("Order shipped email sent")
            
        elif previous_status.lower() == 'shipped' and current_status.lower() == 'delivered':
            print('Your Alsuwaidi package has been delivered.')
            order_url = reverse('order_sucess',  kwargs={'order_id': self.order_id})
            order_page = f"https://suwaidionline.com{order_url}"
            # Send order delivered email
            email_subject = 'Order Delivered'
            email_body = render_to_string('order_delivered_email.html', {
                'order': self,
                'user': self.user,
                'order_id': self.order_id,
                'order_page':order_page,
                'shippingaddress': Address.objects.get(id=self.shipping_address.id),
                # Include other necessary variables for the email body
            })
            safe_email_body = mark_safe(email_body)
            email = EmailMultiAlternatives(
                email_subject,
                body=safe_email_body,
                from_email='settings.ADMIN_EMAIL',
                to=[self.user.email],
            )
            email.attach_alternative(safe_email_body, "text/html")
            email.send()
            print("Order delivered email sent")

        else:
            print("No Email Send")



class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product_name} - Order ID: {self.order.order_id}"
    

class Invoice(models.Model):
    invoice_id = models.CharField(max_length=50)
    invoice_date = models.DateField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    Active = models.BooleanField(default=False)

    def __str__(self):
        return self.invoice_id