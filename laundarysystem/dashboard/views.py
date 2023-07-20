from django.shortcuts import render, get_object_or_404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth import logout
from .forms import *
from base.models import *
from django.contrib import messages
from django.forms import formset_factory
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from .forms import OrderForm
from .forms import CollectionCenterForm
from accounts.models import CustomUser as User
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import user_passes_test
from django.db import IntegrityError

from django.template.loader import render_to_string
from datetime import date, timedelta
from decimal import Decimal
from django.contrib.auth import get_user_model
from django.db.models import Max
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.forms.models import model_to_dict
from .models import Feedback
from .forms import FeedbackForm
from django.http import JsonResponse
from django.db.models import Q






# Create your views here.

def is_admin(user):
    return user.user_type == 'admin'

def is_cc(user):
    return user.user_type == 'collection_center'

def is_user(user):
    return user.user_type == 'user'

@login_required(login_url='account:login')
def home(request):
    if is_admin(request.user):
        order_list = Order.objects.all()
        collection_center_list = CollectionCenter.objects.all()
        user_list = CustomUser.objects.all()
    elif is_cc(request.user):
        collection_center_list = CollectionCenter.objects.get(incharge=request.user)
        order_list = Order.objects.filter(collection_center=collection_center)

        user_list = None

    elif is_user(request.user):
        order_list = Order.objects.filter(user=request.user)
        collection_center_list = None
        user_list = None
    else:
        order_list = None
        collection_center_list = None
        user_list = None

    # Handle None cases and make length 0
    order_list = order_list if order_list is not None else []
    collection_center_list = collection_center_list if collection_center_list is not None else []
    user_list = user_list if user_list is not None else []
   
    clothes_list = Clothes.objects.all()
    cloth_categories_list = Cloth_Category.objects.all()
    subscription_list = Subscription.objects.all()


    clothes_list = clothes_list if clothes_list is not None else []
    subscription_list = subscription_list if subscription_list is not None else []
    cloth_categories_list = cloth_categories_list if cloth_categories_list is not None else []


    order_paginator = Paginator(order_list, 10)  # Set the number of orders per page
    order_page_number = request.GET.get('orders_page')
    orders = order_paginator.get_page(order_page_number)

    collection_center_paginator = Paginator(collection_center_list, 10)  # Set the number of collection centers per page
    collection_center_page_number = request.GET.get('collection_centers_page')
    collection_centers = collection_center_paginator.get_page(collection_center_page_number)

    user_paginator = Paginator(user_list, 10)  # Set the number of users per page
    user_page_number = request.GET.get('users_page')
    users = user_paginator.get_page(user_page_number)

    clothes_paginator = Paginator(clothes_list, 10)  # Set the number of clothes per page
    clothes_page_number = request.GET.get('clothes_page')
    clothes = clothes_paginator.get_page(clothes_page_number)

    cloth_categories_paginator = Paginator(cloth_categories_list, 10)  # Set the number of cloth categories per page
    cloth_categories_page_number = request.GET.get('cloth_categories_page')
    cloth_categories = cloth_categories_paginator.get_page(cloth_categories_page_number)

    subscription_paginator = Paginator(subscription_list, 10)  # Set the number of subscriptions per page
    subscription_page_number = request.GET.get('subscriptions_page')
    subscriptions = subscription_paginator.get_page(subscription_page_number)

    context = { 
        'orders': orders,
        'collection_centers': collection_centers,
        'users': users,
        'clothes': clothes,
        'cloth_categories': cloth_categories,
        'subscriptions': subscriptions
    }

    return render(request=request, template_name='dashboard/home.html', context=context)


def create_order(request, order_id=None):
    collection_centers = CollectionCenter.objects.all()
    clothes = Clothes.objects.all()
    users= User.objects.all()
 
    if order_id:
        order = get_object_or_404(Order, id=order_id)
    else:
        order = None
 
    # breakpoint()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            #order.user = request.user
            order.save()

            data = request.POST
            cloth_items = []
            for key, value in data.items():
                if key.startswith('cloth_'):
                    # form data get using _1 that's last things
                    cloth_id = key.split('_')[1]
                    # also the quantity with _cloth_id which is get from previous code
                    quantity_key = f'quantity_{cloth_id}'
                    quantity = data.get(quantity_key)
                    cloth_items.append((key, value[0], quantity))

            for cloth_item in cloth_items:
                # Create a new OrderItem instance
                cloth=  Clothes.objects.get(pk=cloth_item[1])
                cloth_quantity=Decimal(cloth_item[2])
                order_item = OrderItem(
                    order=order, 
                    cloth_id=cloth_item[1],
                    quantity=cloth_item[2],
                    unit_price=cloth.offer_price,
                    total_price=cloth.offer_price*cloth_quantity

                )
                order_item.save()
    else:
        form = OrderForm(instance=order)
 
    context = {
        'form': form,
        'formset': "formset",
        'order': order,
        'collection_centers': collection_centers,
        'clothes': clothes,
        'users': users,
    }
    return render(request, 'dashboard/create_order.html', context)



def update_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    collection_centers = CollectionCenter.objects.all()
    clothes = Clothes.objects.all()
    users = User.objects.all()

    OrderItemFormSet = inlineformset_factory(Order, OrderItem, fields=('cloth', 'quantity'), extra=1)

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        formset = OrderItemFormSet(request.POST, instance=order)
        if form.is_valid() and formset.is_valid():
            order = form.save()  # Save the main order form data
            formset.save()  # Save the order items formset data

            # Calculate total price for all order items
            order_items = order.orderitem.all()
            for item in order_items:
                item.total_price = item.unit_price * item.quantity
                item.save()

            messages.success(request, 'Order updated successfully.')
            return redirect('dashboard:order_detail', order_id=order_id)
        else:
            messages.error(request, 'Error updating order. Please check the form data.')
    else:
        form = OrderForm(instance=order)
        formset = OrderItemFormSet(instance=order)

    context = {
        'form': form,
        'formset': formset,
        'order': order,
        'collection_centers': collection_centers,
        'clothes': clothes,
        'users': users,
    }
    return render(request, 'dashboard/update_order.html', context)

def create_collection_center(request, collection_center_id=None):
    if not is_admin(request.user):
        return redirect('dashboard:home')
    
    users = User.objects.all().filter(user_type='collection_center')
    collection_center = None
    
    if collection_center_id:
        collection_center = get_object_or_404(CollectionCenter, id=collection_center_id)

    if request.method == 'POST':
        form = CollectionCenterForm(request.POST, instance=collection_center)
        if form.is_valid():
            form.save()
            redirect_url = reverse('dashboard:home') + '#collection-centers'
            return HttpResponseRedirect(redirect_url)

    else:
        form = CollectionCenterForm(instance=collection_center)

    context = {
        'form': form,
        'users': users,
        'collection_center': collection_center
    }
    return render(request, 'dashboard/create_collection_center.html', context)



@login_required
@user_passes_test(is_admin)
def delete_collection_center(request, center_id):
    if not is_admin(request.user):
        return redirect('dashboard:home')
    center = CollectionCenter.objects.get(pk=center_id)
    center.delete()
    redirect_url = reverse('dashboard:home') + '#collection-centers'
    return HttpResponseRedirect(redirect_url)

@login_required
@user_passes_test(is_admin)
def delete_user(request, user_id):
    if not is_admin(request.user):
        return redirect('dashboard:home')
    user = User.objects.get(pk=user_id)
    user.delete()
    redirect_url = reverse('dashboard:home') + '#users'
    return HttpResponseRedirect(redirect_url)

@login_required
@user_passes_test(is_admin)
def delete_cloth(request, cloth_id):
    if not is_admin(request.user):
        return redirect('dashboard:home')
    cloth = Clothes.objects.get(pk=cloth_id)
    cloth.delete()
    redirect_url = reverse('dashboard:home') + '#clothes'
    return HttpResponseRedirect(redirect_url)

@login_required
@user_passes_test(is_admin)
def delete_category(request, category_id):
    # Delete the cloth category object
    if not is_admin(request.user):
        return redirect('dashboard:home')
    category = Cloth_Category.objects.get(pk=category_id)
    category.delete()
    redirect_url = reverse('dashboard:home') + '#cloth-categories'
    return HttpResponseRedirect(redirect_url)

@login_required(login_url='account:login')
def create_cloth(request, cloth_id=None):
    if not is_admin(request.user):
        return redirect('dashboard:home')
    categories = Cloth_Category.objects.all()

    if cloth_id:
        cloth = get_object_or_404(Clothes, id=cloth_id)
    else:
        cloth = None

    if request.method == 'POST':
        form = ClothForm(request.POST, instance=cloth)
        if form.is_valid():
            form.save()
            redirect_url = reverse('dashboard:home') + '#clothes'
            return HttpResponseRedirect(redirect_url)

    else:
        form = ClothForm(instance=cloth)

    context = {
        'form': form,
        'categories': categories,
        'cloth': cloth,
    }
    return render(request, 'dashboard/create_cloth.html', context)

@login_required(login_url='account:login')
def create_category(request, category_id=None):
    if not is_admin(request.user):
        return redirect('dashboard:home')
    if category_id:
        category = get_object_or_404(Cloth_Category, id=category_id)
    else:
        category = None

    if request.method == 'POST':
        form = ClothCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            redirect_url = reverse('dashboard:home') + '#cloth-categories'
            return HttpResponseRedirect(redirect_url)

    else:
        form = ClothCategoryForm(instance=category)

    context = {
        'form': form,
        'is_update': category_id is not None,
        'category': category,
    }
    return render(request, 'dashboard/create_category.html', context)


@login_required(login_url='account:login')
def create_subscription(request, subscription_id=None):
    if not is_admin(request.user):
        return redirect('dashboard:home')
    if subscription_id:
        subscription = get_object_or_404(Subscription, id=subscription_id)
    else:
        subscription = None

    if request.method == 'POST':
        form = SubscriptionForm(request.POST, instance=subscription)
        if form.is_valid():
            form.save()
            redirect_url = reverse('dashboard:home') + '#subscriptions'
            return HttpResponseRedirect(redirect_url)
    else:
        form = SubscriptionForm(instance=subscription)

    context = {
        'form': form,
        'subscription': subscription,
    }
    return render(request, 'dashboard/create_subscription.html', context)


@login_required
#@user_passes_test(is_admin)
def delete_subscription(request, subscription_id):
    if not is_admin(request.user):
        return redirect('dashboard:home')
    # Delete the cloth category object
    subs = Subscription.objects.get(pk=subscription_id)
    subs.delete()
    redirect_url = reverse('dashboard:home') + '#subscriptions'
    return HttpResponseRedirect(redirect_url)

@login_required(login_url='account:login')
def order_details(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if is_user(request.user) and order.user  != request.user:
        return redirect('dashboard:home')
    order_total = sum(item.cloth.offer_price * item.quantity for item in order.orderitem.all())
    invoice = Invoice.objects.filter(order=order).first()

    feedback = Feedback.objects.filter(order=order)


    context = {
        'order': order,
        'order_total': order_total,
        'invoice': invoice,
        'feedback': feedback,

    }
    return render(request, 'dashboard/order_details.html', context)



@login_required(login_url='account:login')
def change_order_status(request, order_id):
    if is_user(request.user) and order.user  != request.user:
        return redirect('dashboard:home')
    status = request.GET.get('status')
    order = get_object_or_404(Order, id=order_id)

    if is_cc(request.user) and order.collection_center != request.user: 
        return redirect('dashboard:home')

    # Update the order status based on the received status value
    order.status = status
    order.save()

    if status == 'placed':
        # Check if an invoice already exists for the order
        existing_invoice = Invoice.objects.filter(order=order).first()
        User = get_user_model()
        user = User.objects.get(id=request.user.id)
        #user = User().objects.get(id=order.user_id)

        if existing_invoice:
            # Update the existing invoice
            existing_invoice.issue_date = date.today()
            existing_invoice.due_date = date.today() + timedelta(days=7)
            existing_invoice.total_amount = calculate_total_amount(order) 
            existing_invoice.save()
            invoice = existing_invoice
        else:
            # Generate the invoice
            max_invoice_number = Invoice.objects.aggregate(max_invoice_number=Max('invoice_number'))['max_invoice_number']
    
            # Determine the next invoice number
            if max_invoice_number:
                next_invoice_number = int(max_invoice_number[3:]) + 1
            else:
                next_invoice_number = 1
            
            # Format the invoice number with leading zeros
            invoice_number = f"INV{next_invoice_number:04}"
            
            invoice = Invoice.objects.create(
                order=order,
                invoice_number=invoice_number,
                issue_date=date.today(),
                due_date=date.today() + timedelta(days=7),
                total_amount=calculate_total_amount(order),
                payment_status='Pending',  # Initial payment status
                payment_method='',  # Set as per your implementation
                billing_name=f"{user.first_name} {user.last_name}",  # Set as per your implementation
                billing_address=order.pickup_location,  # Set as per your implementation
                billing_contact= user.phone_number,  # Set as per your implementation
                notes='',  # Set as per your implementation
            )

        # Redirect to the invoice detail page
        return redirect('dashboard:invoice_details', invoice_id=invoice.id)
    else:
        # Redirect to the order detail page
        return redirect('dashboard:order_details', order_id=order.id)


@login_required(login_url='account:login')
def create_or_update_user(request, user_id=None):
    
    user = get_object_or_404(CustomUser, id=user_id) if user_id else None
    if is_user(request.user) and user==None and request.user != user:
            return redirect('dashboard:home')
    subscriptions = Subscription.objects.all()
    account_status_choices = CustomUser.VERIFICATION_STATUS

    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            try:
                form.save()
                if user_id:
                    messages.success(request, 'User details updated successfully.')
                else:
                    messages.success(request, 'User created successfully.')
                return redirect('account:user_account')
            except IntegrityError:
                messages.error(request, 'User with the same phone number already exists.')
    else:
        form = UserForm(instance=user)

    context = {
        'form': form,
        'user': user,
        'subscriptions': subscriptions,
        'account_status_choices': account_status_choices,
    }
    return render(request, 'dashboard/create_user.html', context)

@login_required(login_url='account:login')
def calculate_total_amount(order):
    total_amount = 0
    order_items = OrderItem.objects.filter(order=order)
    for order_item in order_items:
        total_amount += order_item.total_price
    return total_amount

@login_required(login_url='account:login')
def invoice_details(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)

    context = {
        'invoice': invoice
    }
    return render(request, 'dashboard/invoice_details.html', context)

@login_required(login_url='account:login')
def pay_invoice(request, invoice_id):
    if is_user(request.user):
        return redirect('dashboard:home')
    invoice = get_object_or_404(Invoice, id=invoice_id)
    
    # Check if the invoice is already paid
    if invoice.payment_status == 'Paid':
        return HttpResponse('This invoice is already paid.')
    
    # Process the payment logic here
    # ...

    # Update the invoice payment status
    invoice.payment_status = 'Paid'
    invoice.save()

    # Redirect to a success page or display a success message
    return HttpResponse('Payment successful. Thank you!')


@login_required(login_url='account:login')
def send_email(subject, message, to_email):
    send_mail(
        subject,
        message,
        'admin@email.com',
        [to_email],
        fail_silently=False,
        )




def submit_feedback(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    if request.method == 'POST':
        form = FeedbackForm(request.POST, request.FILES)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.order = order
            feedback.user = request.user
            feedback.save()
            return redirect('dashboard:order_details', order_id=order_id)
    else:
        form = FeedbackForm()
    
    return render(request, 'dashboard/feedback.html', {'form': form, 'order': order})



def user_search(request):
    if request.method == 'GET':
        query = request.GET.get('q', '')
        users = User.objects.filter(Q(first_name__icontains=query) | Q(last_name__icontains=query) | Q(phone_number__icontains=query))
        results = [
            {
                'id': user.id,
                'text': f'{user.first_name} {user.last_name} - {user.phone_number}'
            }
            for user in users
        ]
        return JsonResponse(results, safe=False)
    

