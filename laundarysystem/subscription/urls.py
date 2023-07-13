from django.urls import path
from subscription.views import create_pickup_request

app_name = 'subscription'

urlpatterns = [
    path('create_pickup_request/', create_pickup_request, name='create_pickup_request'),
]
