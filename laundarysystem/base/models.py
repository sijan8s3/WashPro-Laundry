from django.db import models
from django.conf import settings


# Create your models here.

class Cloth_Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Clothes(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(
        Cloth_Category, on_delete=models.SET_NULL, null=True)
    reg_price = models.DecimalField(max_digits=6, decimal_places=2)
    offer_price = models.DecimalField(
        max_digits=6, decimal_places=2, null=True)
    update = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Subscription(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    pickup = models.IntegerField()
    validity = models.IntegerField()
    weight = models.DecimalField(max_digits=8, decimal_places=2)
    update = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class CollectionCenter(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=500, null=True, blank=True)
    description = models.CharField(max_length=500, null=True, blank=True)
    active = models.BooleanField(default=False)
    incharge = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    update = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    ORDER_STATUS = (
        ('draft', 'Pending'),
        ('placed', 'Order Placed'),
        ('collected', 'Collected'),
        ('washing', 'Washing'),
        ('delivered_cc', 'Delivered to Collection'),
        ('delivery_ready', 'Out for Delivery'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    collection_center = models.ForeignKey(
        CollectionCenter, on_delete=models.CASCADE)
    pickup_location = models.CharField(max_length=200)
    pickup_date = models.DateField()
    status = models.CharField(
        max_length=20, choices=ORDER_STATUS, default='pending')
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.pk}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="orderitem")
    cloth = models.ForeignKey(
        Clothes, on_delete=models.CASCADE, related_name="cloth")
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    total_price = models.DecimalField(max_digits=6, decimal_places=2, null=True)

    def __str__(self):
        return f"{self.order} - {self.cloth}"


class Invoice(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    invoice_number = models.CharField(max_length=50, unique=True)
    issue_date = models.DateField()
    due_date = models.DateField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=20)
    payment_method = models.CharField(max_length=50)
    billing_name = models.CharField(max_length=100)
    billing_address = models.CharField(max_length=200)
    billing_contact = models.CharField(max_length=20)
    notes = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.invoice_number
    


