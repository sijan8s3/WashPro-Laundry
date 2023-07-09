from django import forms
from django.forms import formset_factory
from base.models import *
from accounts.models import *
from django.core.exceptions import ValidationError


'''
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

'''

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
        fields = ['collection_center', 'pickup_location', 'pickup_date']

OrderItemFormSet = inlineformset_factory(Order, OrderItem, fields=('cloth', 'quantity'), extra=1)


class UserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'address', 'current_subscription', 'is_staff']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['current_subscription'].required = False
        self.fields['is_staff'].disabled = True

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        if CustomUser.objects.filter(phone_number=phone_number).exists():
            raise ValidationError("A user with this phone number already exists.")
        return phone_number