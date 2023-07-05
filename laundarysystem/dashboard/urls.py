from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.home, name='home'),
    path('order/create/', views.create_order, name='create_order'),
    path('order/<str:pk>/', views.order_detail, name='orderdetail'),
    
    
]