from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.home, name='home'),
    path('order/create/', views.create_order, name='create_order'),
    path('order/<str:pk>/', views.order_detail, name='orderdetail'),
    
    path('collection_center/create/', views.create_collection_center, name='create_collection_center'),
    path('collection_center/<int:collection_center_id>/update/', views.create_collection_center, name='update_collection_center'),
    path('collection_center/delete/<int:center_id>/', views.delete_collection_center, name='delete_collection_center'),
    
    path('user/delete/<int:user_id>/', views.delete_user, name='delete_user'),

    path('cloth/create/', views.create_cloth, name='create_cloth'),
    path('cloth/<int:cloth_id>/update', views.create_cloth, name='update_cloth'),
    path('cloth/delete/<int:cloth_id>/', views.delete_cloth, name='delete_cloth'),
    
    path('category/create/', views.create_category, name='create_category'),
    path('category/<int:category_id>/update', views.create_category, name='update_category'),
    path('delete_category/<int:category_id>/', views.delete_category, name='delete_category'),


]