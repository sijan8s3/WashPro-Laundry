from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm


from .models import CustomUser

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField()
    phone_number = forms.CharField(max_length=10)

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'phone_number', 'password1', 'password2')

    ''' def save(self, commit=True):
        user = CustomUser.objects.create_user(
            phone_number=self.cleaned_data['phone_number'],
            password=self.cleaned_data['password1'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            email=self.cleaned_data['email']
        )
        return user '''
    
    def save(self, commit=True):
            user = super().save(commit=False)
            user.phone_number = self.cleaned_data['phone_number']
            if commit:
                user.save()
            return user


class UserDetailsForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'address']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Customize form fields if needed
        self.fields['address'].widget.attrs['rows'] = 3

class ChangePasswordForm(PasswordChangeForm):
    class Meta:
        model = CustomUser