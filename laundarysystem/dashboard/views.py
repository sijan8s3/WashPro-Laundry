from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth import logout
from .forms import OrderForm, OrderClothForm, OrderClothFormSet, ClothForm, ClothCategoryForm, SubscriptionForm
from base.models import Order, Clothes, CollectionCenter, Cloth_Category, OrderItem, Subscription
from django.contrib import messages
from accounts.models import CustomUser
from django.forms import formset_factory
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from .forms import OrderForm
from .forms import CollectionCenterForm
from accounts.models import CustomUser as User
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import user_passes_test




# Create your views here.

def is_admin(user):
    return user.user_type == 'admin'

@login_required(login_url='account:login')
def home(request):
    orders = Order.objects.all()
    collection_centers = CollectionCenter.objects.all()
    users = CustomUser.objects.all()
    clothes = Clothes.objects.all()
    cloth_categories = Cloth_Category.objects.all()
    subscriptions = Subscription.objects.all()
    context= { 
        'orders': orders,
        'collection_centers': collection_centers,
        'users': users,
        'clothes': clothes,
        'cloth_categories': cloth_categories,
        'subscriptions': subscriptions
    }
    return render(request=request, template_name='dashboard/home.html', context=context)


def create_order(request):
    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        formset = OrderClothFormSet(request.POST)

        if order_form.is_valid():
            order = order_form.save(commit=False)
            order.user = request.user
            order.save()
        else:
            print(order_form.errors)

        if formset.is_valid():
            # Process the formset
            print('nice')
        else:
            print(formset.errors)


        if order_form.is_valid() and formset.is_valid():
            order = order_form.save(commit=False)
            order.user = request.user
            order.save()

            for form in formset:
                cloth = form.cleaned_data['cloth']
                quantity = form.cleaned_data['quantity']
                OrderItem.objects.create(order=order, cloth=cloth, quantity=quantity)

            messages.success(request, 'Order created successfully.')
            return redirect('dashboard:order_detail', pk=order.pk)
        else:
            messages.error(request, 'Failed to create the order. Please check the form.')

    else:
        order_form = OrderForm()
        formset = OrderClothFormSet()
    clothes = Clothes.objects.all()
    context = {
        'order_form': order_form,
        'formset': formset,
        'clothes': clothes,
    }

    return render(request, 'dashboard/create_order.html', context)



def create_collection_center(request, collection_center_id=None):
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
    center = CollectionCenter.objects.get(pk=center_id)
    center.delete()
    redirect_url = reverse('dashboard:home') + '#collection-centers'
    return HttpResponseRedirect(redirect_url)

@login_required
@user_passes_test(is_admin)
def delete_user(request, user_id):
    user = User.objects.get(pk=user_id)
    user.delete()
    redirect_url = reverse('dashboard:home') + '#users'
    return HttpResponseRedirect(redirect_url)

#@login_required
#@user_passes_test(is_admin)
def delete_cloth(request, cloth_id):
    cloth = Clothes.objects.get(pk=cloth_id)
    cloth.delete()
    redirect_url = reverse('dashboard:home') + '#clothes'
    return HttpResponseRedirect(redirect_url)

@login_required
#@user_passes_test(is_admin)
def delete_category(request, category_id):
    # Delete the cloth category object
    category = Cloth_Category.objects.get(pk=category_id)
    category.delete()
    redirect_url = reverse('dashboard:home') + '#cloth-categories'
    return HttpResponseRedirect(redirect_url)


def create_cloth(request, cloth_id=None):
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


def create_category(request, category_id=None):
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



def create_subscription(request, subscription_id=None):
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
    # Delete the cloth category object
    subs = Subscription.objects.get(pk=subscription_id)
    subs.delete()
    redirect_url = reverse('dashboard:home') + '#subscriptions'
    return HttpResponseRedirect(redirect_url)


def order_details(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order_total = sum(item.cloth.offer_price * item.quantity for item in order.orderitem_set.all())
    
    context = {
        'order': order,
        'order_total': order_total,
    }
    return render(request, 'dashboard/order_details.html', context)


