from django import forms
from subscription.models import PickupRequest

class PickupRequestForm(forms.ModelForm):
    class Meta:
        model = PickupRequest
        fields = ['collection_center', 'pickup_location', 'pickup_date']
        widgets = {
            'pickup_date': forms.DateInput(attrs={'type': 'date'})
        }
