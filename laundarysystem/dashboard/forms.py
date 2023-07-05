from django import forms
from django.forms import formset_factory
from base.models import Order, Clothes, CollectionCenter, OrderItem

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('collection_center',)

class OrderClothForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ('cloth', 'quantity')

OrderClothFormSet = formset_factory(OrderClothForm, extra=1)
