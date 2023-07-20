from django.db import models
from django.conf import settings
from base.models import Order

# Create your models here.

class Feedback(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    feedback_text = models.TextField()
    image = models.ImageField(upload_to='feedback_images/', null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback for Order {self.order.id} by {self.user.phone_number}"
