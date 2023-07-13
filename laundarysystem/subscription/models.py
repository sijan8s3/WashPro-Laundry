from django.db import models
from base.models import *
from django.contrib.auth import get_user_model
from django.utils import timezone


User = get_user_model()


# Create your models here.

class UserSubscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subscription_plan = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()

    def remaining_pickups(self):
    # Get the pickup requests within the subscription dates
        pickup_requests = self.pickuprequest_set.filter(created__gte=self.start_date, created__lte=self.end_date)
        return self.subscription_plan.maximum_pickups - pickup_requests.count()
    
    def remaining_cloth_weight(self):
        # Get the total cloth weight of pickup requests within the subscription dates
        total_weight = self.pickuprequest_set.filter(created__gte=self.start_date, created__lte=self.end_date).aggregate(models.Sum('cloth_weight'))['cloth_weight__sum']
        if total_weight:
            return self.subscription_plan.maximum_cloth_weight - total_weight
        return self.subscription_plan.maximum_cloth_weight
    
    @property
    def has_expired(self):
        return self.end_date < timezone.now().date()

    def __str__(self):
        return f"{self.user.first_name}'s Subscription"


class PickupRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pickup_location = models.CharField(max_length=200)
    collection_center = models.ForeignKey(CollectionCenter, on_delete=models.SET_NULL, null=True)
    cloth_weight = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    pickup_date = models.DateField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)

    STATUS_CHOICES = (
        ('requested', 'Requested'),
        ('collecting', 'Collecting'),
        ('collected', 'Collected'),
        ('order_created', 'Order Created'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='requested', null=True)



    def __str__(self):
        return f"Pickup Request by {self.user.first_name} on {self.pickup_date}"
