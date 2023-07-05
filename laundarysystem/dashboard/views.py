from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth import logout
from .forms import OrderForm, OrderClothForm, OrderClothFormSet
from base.models import Order, Clothes, OrderItem
from django.contrib import messages
from django.forms import formset_factory




# Create your views here.

@login_required(login_url='account:login')
def home(request):
    context= {'user': request.user}
    return render(request=request, template_name='dashboard/home.html', context=context)


def create_order(request):
    OrderClothFormSet = formset_factory(OrderClothForm, extra=1)
    
    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        order_cloth_formset = OrderClothFormSet(request.POST)
        
        if order_form.is_valid() and order_cloth_formset.is_valid():
            order = order_form.save(commit=False)
            order.user = request.user
            order.status = "pending"
            order.save()
            
            for form in order_cloth_formset:
                cloth = form.cleaned_data['cloth']
                quantity = form.cleaned_data['quantity']
                OrderItem.objects.create(order=order, cloth=cloth, quantity=quantity)
            
            return redirect('dashboard:order_detail', order_id=order.pk)
        else:
            error_message = 'Error occurred while adding the order.'
            messages.error(request, error_message)
    else:
        order_form = OrderForm()
        order_cloth_formset = OrderClothFormSet()
    
    clothes = Clothes.objects.all()
    
    return render(request, 'dashboard/create_order.html', {
        'order_form': order_form,
        'order_cloth_formset': order_cloth_formset,
        'clothes': clothes,
    })



def order_detail(request, order_id):
    order = Order.objects.get(pk=order_id)
    return render(request, 'dashboard/order_detail.html', {'order': order})
