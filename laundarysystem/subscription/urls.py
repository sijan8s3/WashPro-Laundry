from django.urls import path
from subscription import views

app_name = 'subscription'

urlpatterns = [
    path('create_pickup_request/', views.create_pickup_request, name='create_pickup_request'),
    path('pickup_request_success/', views.pickup_request_success, name='pickup_request_success'),

]
