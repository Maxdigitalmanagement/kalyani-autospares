from django.db import models
from accounts.models import Account,UserAddress
from store.models import Product, Variation
import pytz
from django.utils import timezone
# Create your models here.


class Payment(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=100)
    amount_paid = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.payment_id
    


class Order(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Processing', 'Processing'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    order_number = models.CharField(max_length=20)
    address = models.ForeignKey(UserAddress, on_delete=models.SET_NULL, null=True)
    order_note = models.CharField(max_length=100,blank=True)
    order_total = models.FloatField()
    tax = models.FloatField()
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    ip = models.CharField(blank=True, max_length=20)
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def full_name(self):
        return f'{self.address.first_name} {self.address.last_name}'
    
    def first_name(self):
        return f'{self.address.first_name}'
    def last_name(self):
        return f'{self.address.last_name}'
    def email(self):
        return f'{self.address.email}'
    def phone(self):
        return f'{self.address.phone}'
    def city(self):
        return f'{self.address.city}'
    def address_line_1(self):
        return f'{self.address.address_line_1}'
    def address_line_2(self):
        return f'{self.address.address_line_2}'
    def pincode(self):
        return f'{self.address.pincode}'
    def state(self):
        return f'{self.address.state}'
    def country(self):
        return f'{self.address.country}'
    
    def date(self):
        order_created = self.created_at

        # Get the Asia/Kolkata timezone
        kolkata_timezone = pytz.timezone('Asia/Kolkata')

        # Convert the 'order_created' datetime to the Kolkata timezone
        order_created_kolkata = timezone.localtime(order_created, timezone=kolkata_timezone)

        # Format the 'order_created_kolkata' in the desired format
        formatted_order_created_kolkata = order_created_kolkata.strftime('%B %d, %Y @ %I:%M %p')
        return f'{formatted_order_created_kolkata}'
    
    def ordered_date(self):
        order_date = self.created_at.strftime('%d/%m/%Y')
        return f'{order_date}'
    
    def order_quantity(self):
        qty = 0
        order_prd = OrderProduct.objects.filter(user=self.user,order_id=self.id)
        for order in order_prd:
            qty +=order.quantity
        return qty
    
    def order_subtotal(self):
        sub = 0
        order_prd = OrderProduct.objects.filter(user=self.user,order_id=self.id)
        for order in order_prd:
            sub +=order.quantity*order.product_price
        return sub

    def __str__(self):
        return self.user.first_name
    


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variations = models.ManyToManyField(Variation, blank=True)
    quantity = models.IntegerField()
    product_price = models.FloatField()
    ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.product_name
    
    def sub_total(self):
        return self.product_price*self.quantity