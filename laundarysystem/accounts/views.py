from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .forms import SignUpForm
from django.contrib.auth import get_user_model
from django.conf import settings
from accounts.models import CustomUser
from django.contrib.auth.forms import PasswordChangeForm
from .forms import UserDetailsForm
from django.contrib.auth import update_session_auth_hash
from .forms import UserDetailsForm, ChangePasswordForm







# Create your views here.
def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard:home')

    if request.method == 'POST':
        phone_number = request.POST['phone_number']
        password = request.POST['password']
        user = authenticate(request, phone_number=phone_number, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard:home')
        else:
            try:
                user = User.objects.get(phone_number=phone_number)
                messages.error(request, 'Invalid password.')
            except User.DoesNotExist:
                messages.error(request, 'Invalid phone number.')

    return render(request, 'account/login.html')


def logout_view(request):
    logout(request)
    return redirect('home')


User = get_user_model()

def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            CustomUser.objects.create_user(first_name=first_name, last_name=last_name, phone_number=phone_number, email=email, password=password)
            return redirect('account:login')
    else:
        form = SignUpForm()
    return render(request, 'account/register.html', {'form': form})


@login_required
def user_account(request):
    if request.method == 'POST':
        user_details_form = UserDetailsForm(request.POST, instance=request.user)
        password_change_form = PasswordChangeForm(user=request.user, data=request.POST)

        if user_details_form.is_valid():
            user_details_form.save()
            messages.success(request, 'User details updated successfully.')
            return redirect('account:user_account')

        if password_change_form.is_valid():
            user = password_change_form.save()
            update_session_auth_hash(request, user)  # To keep the user logged in
            messages.success(request, 'Password changed successfully.')
            return redirect('account:user_account')

    else:
        user_details_form = UserDetailsForm(instance=request.user)
        password_change_form = PasswordChangeForm(user=request.user)

    context = {
        'user_details_form': user_details_form,
        'password_change_form': password_change_form,
    }

    return render(request, 'account/user_account.html', context)


@login_required
def update_details(request):
    user = request.user

    if request.method == 'POST':
        user_form = UserDetailsForm(request.POST, instance=user)

        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'User details updated successfully.')
            return redirect('account:user_account')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        user_form = UserDetailsForm(instance=user)

    context = {
        'user_form': user_form,
    }
    return render(request, 'account/user_account.html', context)

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password has been changed successfully.')
            return redirect('account:user_account')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'account/change_password.html', {'form': form})