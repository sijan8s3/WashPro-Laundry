from django.shortcuts import render, redirect
from subscription.models import UserSubscription
from .forms import *
from django.contrib.auth.decorators import login_required
from base.models import CollectionCenter


@login_required
def create_pickup_request(request):
    user = request.user
    user_subscription = UserSubscription.objects.get(user=user)
    collection_centers = CollectionCenter.objects.all()  # Retrieve all collection centers

    if user_subscription.has_expired:
        return render(request, 'subscription/subscription_expired.html')
    
    if request.method == 'POST':
        form = PickupRequestForm(request.POST)
        if form.is_valid():
            # Create the pickup request object
            pickup_request = form.save(commit=False)
            pickup_request.user = user
            pickup_request.save()
        
            
            return redirect('subscription:pickup_request_success')
    else:
        form = PickupRequestForm()
    
    return render(request, 'subscription/create_pickup_request.html', {'user_subscription': user_subscription, 'form': form, 'collection_centers': collection_centers})