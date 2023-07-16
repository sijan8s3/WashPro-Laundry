from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('base.urls')),
    path('accounts/', include('accounts.urls', namespace='account')),
    path('dashboard/', include('dashboard.urls', namespace='dashboard')),
    path('subscription/', include('subscription.urls', namespace='subscription')),
    path('khalti/', include('khalti.urls')),



]

