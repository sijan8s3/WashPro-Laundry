from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from base.models import Subscription
from .managers import CustomUserManager
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin



# Create your models here.

class CustomUser(AbstractBaseUser, PermissionsMixin):
    USER_TYPE_CHOICES = (
        ('admin', 'Admin'),
        ('collection_center', 'Collection Center'),
        ('user', 'User'),
    )

    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='user')

    VERIFICATION_STATUS = (
        ('verfied', 'Verified'),
        ('not_verified', 'Not Verified')
    )
    account_status = models.CharField(max_length=20, choices=VERIFICATION_STATUS, default='not_verified')

    phone_number = models.CharField(max_length=10,  unique=True, blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    current_subscription = models.ForeignKey(Subscription, on_delete=models.SET_NULL, null=True, blank=True) 
    is_staff = models.BooleanField(default=False)
    first_name = models.CharField(max_length=200, blank=True, null=True)
    last_name = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(max_length=200, blank=True, null=True)



    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']


    objects = CustomUserManager()

