from django.db import models
from user.models import *
from product.models import *
from checkout.models import *

# Create your models here.
class GiftCard(models.Model):
    number = models.CharField(max_length=50, unique=True)
    active = models.BooleanField(default=True)
    create_date = models.DateTimeField(auto_now_add=True)
    expiration_date = models.DateField()
    gift_card_parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    recipient_email = models.EmailField()
    recipient_name = models.CharField(max_length=100)
    from_name = models.CharField(max_length=100)
    message = models.TextField()
    delivery_date = models.DateField()
    email_design_id = models.IntegerField()
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    # variation_id = models.ForeignKey('ProductVariation', on_delete=models.CASCADE)
    order_item_id = models.ForeignKey(OrderItem, on_delete=models.CASCADE)

    def __str__(self):
        return self.number

class GiftCardActivity(models.Model):
    ACTION_CHOICES = [
        ('created', 'Created'),
        ('redeemed', 'Redeemed'),
        ('refunded', 'Refunded'),
    ]

    gift_card = models.ForeignKey(GiftCard, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity_date = models.DateTimeField(auto_now_add=True)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    note = models.TextField()
    reference_activity_id = models.IntegerField()

    def __str__(self):
        return f"{self.action} - {self.gift_card.number}"