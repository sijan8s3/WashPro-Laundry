from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name="register"),
    path('logout/', views.logout_view, name='logout'),
    path('user-account/', views.user_account, name='user_account'),
    path('update-details/', views.update_details, name='update_details'),
    path('change-password/', views.change_password, name='change_password'),


    
]