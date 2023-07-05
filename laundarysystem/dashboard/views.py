from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth import logout
from .forms import OrderForm, OrderClothForm, OrderClothFormSet
from base.models import Order, Clothes, CollectionCenter
from django.contrib import messages
from accounts.models import CustomUser
from django.forms import formset_factory



# Create your views here.

@login_required(login_url='account:login')
def home(request):
    orders = Order.objects.all()
    collection_centers = CollectionCenter.objects.all()
    users = CustomUser.objects.all()
    context= { 
        'orders': orders,
        'collection_centers': collection_centers,
        'users': users,
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



def order_detail(request, order_id):
    order = Order.objects.get(pk=order_id)
    return render(request, 'dashboard/order_detail.html', {'order': order})
