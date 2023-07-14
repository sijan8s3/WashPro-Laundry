from django.shortcuts import render, redirect, get_object_or_404
from subscription.models import UserSubscription
from .forms import *
from django.contrib.auth.decorators import login_required
from base.models import CollectionCenter, Order
from django.contrib import messages
from django.http import HttpResponseBadRequest
from django.urls import reverse



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


def pickup_request_success(request):
    return render(request, 'subscription/pickup_request_success.html')


def update_pickup_request_status(request, request_id):
    pickup_request = get_object_or_404(PickupRequest, id=request_id)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        pickup_request.status = new_status
        pickup_request.save()

        if new_status == 'collected':
            # Create an order based on the pickup request
            order = Order.objects.create(
                user=pickup_request.user,
                collection_center=pickup_request.collection_center,
                pickup_location=pickup_request.pickup_location,
                pickup_date=pickup_request.pickup_date,
                status='collected',
                order_type='subscription'  # Set the order type as needed
            )
            pickup_request.order = order
            pickup_request.save()

            # Perform other necessary actions for order creation

        # Redirect to the pickup request detail page or any other desired page
        return render(request, 'subscription/pickup_request_detail.html', {'pickup_request': pickup_request})

    # Handle GET request if needed

    # Render a template with form to update the status
    return render(request, 'subscription/pickup_request_detail.html', {'pickup_request': pickup_request})

def pickup_request_detail(request, pickup_request_id):
    pickup_request = get_object_or_404(PickupRequest, id=pickup_request_id)
    return render(request, 'subscription/pickup_request_detail.html', {'pickup_request': pickup_request})



def update_cloth_weight(request, request_id):
    pickup_request = get_object_or_404(PickupRequest, id=request_id)
    
    if request.method == 'POST':
        cloth_weight = request.POST.get('cloth_weight')
        if cloth_weight is None:
            messages.error(request, 'Invalid cloth weight.')
            return redirect('subscription:pickup_request_detail', request_id=pickup_request.id)
        
        # Update the cloth weight of the pickup request
        pickup_request.cloth_weight = cloth_weight
        pickup_request.status = 'order_created'
        pickup_request.save()
        
        # Show a success message
        messages.success(request, 'Cloth weight updated successfully.')
        
        # Redirect back to the pickup request detail page
        return redirect(reverse('subscription:pickup_request_detail', kwargs={'pickup_request_id': pickup_request.id}))
    
    # Handle GET request if needed
    
    # Render a template for updating cloth weight (if required)
    return render(request, 'subscription/update_cloth_weight.html', {'pickup_request': pickup_request})


@login_required
def user_home(request):
    user = request.user
    user_subscription = UserSubscription.objects.filter(user=user).first()
    last_pickup = PickupRequest.objects.filter(user=user).order_by('-created').first()
    last_order = Order.objects.filter(user=user).order_by('-created').first()

    return render(request, 'subscription/user_home.html', {
        'user': user,
        'user_subscription': user_subscription,
        'last_pickup': last_pickup,
        'last_order': last_order
    })