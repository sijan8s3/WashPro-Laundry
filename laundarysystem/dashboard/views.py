from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth import logout
from .forms import OrderForm, OrderClothForm, OrderClothFormSet
from base.models import Order, Clothes, CollectionCenter
from django.contrib import messages
from accounts.models import CustomUser



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
        order_cloth_formset = OrderClothFormSet(request.POST)
        if order_form.is_valid() and order_cloth_formset.is_valid():
            order = order_form.save(commit=False)
            order.user = request.user
            order.save()
            order_cloth_formset.instance = order
            order_cloth_formset.save()
            return redirect('dashboard:order_detail', order_id=order.pk)
        else:
            messages.error(request, 'Error occurred while adding the order.')
    else:
        order_form = OrderForm()
        order_cloth_formset = OrderClothFormSet()
    
    clothes = Clothes.objects.all()  # Get all clothes from the database
    
    return render(request, 'dashboard/create_order.html', {
        'order_form': order_form,
        'order_cloth_formset': order_cloth_formset,
        'clothes': clothes  # Pass the clothes to the template
    })

def order_detail(request, order_id):
    order = Order.objects.get(pk=order_id)
    return render(request, 'dashboard/order_detail.html', {'order': order})
