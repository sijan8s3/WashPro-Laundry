from django import forms
from django.forms import formset_factory
from base.models import Order, OrderItem, CollectionCenter, Clothes, Cloth_Category, Subscription


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



class CollectionCenterForm(forms.ModelForm):
    class Meta:
        model = CollectionCenter
        fields = ['name', 'address', 'description', 'active', 'incharge']


class ClothForm(forms.ModelForm):
    class Meta:
        model = Clothes
        fields = ['name', 'category', 'reg_price', 'offer_price']


class ClothCategoryForm(forms.ModelForm):
    class Meta:
        model = Cloth_Category
        fields = ['name']


class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ['name', 'price', 'pickup', 'validity', 'weight']
        


from django.forms import inlineformset_factory

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['collection_center', 'pickup_location', 'pickup_date', 'status']
        widgets = {
            'status': forms.HiddenInput(attrs={'value': 'pending'}),
        }

OrderItemFormSet = inlineformset_factory(Order, OrderItem, fields=('cloth', 'quantity'), extra=1)

