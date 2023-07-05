from django import forms
from django.forms import formset_factory
from base.models import Order, OrderItem

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('collection_center', 'pickup_location', 'pickup_date')
        
    def clean(self):
        cleaned_data = super().clean()
        pickup_location = cleaned_data.get('pickup_location')
        pickup_date = cleaned_data.get('pickup_date')
        
        if not pickup_location or not pickup_date:
            raise forms.ValidationError("Please fill in all the required fields.")

class OrderClothForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ('cloth', 'quantity')

OrderClothFormSet = formset_factory(OrderClothForm, extra=1)
