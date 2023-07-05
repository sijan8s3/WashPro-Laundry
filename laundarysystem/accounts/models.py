from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class CustomUser(AbstractUser):
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
