from django.db import models
from base.models import *
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db.models import Q, Sum


User = get_user_model()


# Create your models here.

class UserSubscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subscription_plan = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()

    @property
    def remaining_pickups(self):
        start_date = self.start_date
        end_date = self.end_date
    # Get the pickup requests within the subscription dates
        pickup_requests = self.user.pickuprequest_set.filter(
            ~Q(status='cancelled'), pickup_date__range=(start_date, end_date)
        )
        return self.subscription_plan.pickup - pickup_requests.count()

    
    @property
    def remaining_cloth_weight(self):
        # Get the total cloth weight of pickup requests within the subscription dates
        total_weight = PickupRequest.objects.filter(
            user=self.user,
            created__gte=self.start_date,
            created__lte=self.end_date
        ).exclude(status='cancelled').aggregate(total_weight=Sum('cloth_weight'))['total_weight']
        if total_weight:
            return self.subscription_plan.weight - total_weight
        return self.subscription_plan.weight
    
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
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    STATUS_CHOICES = (
        ('requested', 'Requested'),
        ('collecting', 'Collecting'),
        ('collected', 'Collected'),
        ('order_created', 'Order Created'),
        ('cancelled', 'Cancelled'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='requested', null=True)



    def __str__(self):
        return f"Pickup Request by {self.user.first_name} on {self.pickup_date}"

    


