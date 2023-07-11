from django.contrib import admin
from .models import *
from accounts.models import CustomUser

# Register your models here.

admin.site.register(Cloth_Category)
admin.site.register(Clothes)
admin.site.register(Subscription)
admin.site.register(CollectionCenter)
admin.site.register(CustomUser)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Invoice)

