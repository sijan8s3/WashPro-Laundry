from django.urls import path
from subscription import views

app_name = 'subscription'

urlpatterns = [
    path('create_pickup_request/', views.create_pickup_request, name='create_pickup_request'),
    path('pickup_request_success/', views.pickup_request_success, name='pickup_request_success'),
    path('update_pickup_request_status/<int:request_id>/', views.update_pickup_request_status, name='update_pickup_request_status'),
    path('pickup_request_detail/<int:pickup_request_id>/', views.pickup_request_detail, name='pickup_request_detail'),
    path('update_cloth_weight/<int:request_id>/', views.update_cloth_weight, name='update_cloth_weight'),

    path('user_home/', views.user_home, name='user_home'),


]
