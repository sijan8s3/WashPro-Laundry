from django.contrib import admin
from .models import Cloth_Category, Clothes, Subscription, CollectionCenter, Order
from accounts.models import CustomUser

# Register your models here.

admin.site.register(Cloth_Category)
admin.site.register(Clothes)
admin.site.register(Subscription)
admin.site.register(CollectionCenter)
admin.site.register(CustomUser)
admin.site.register(Order)

