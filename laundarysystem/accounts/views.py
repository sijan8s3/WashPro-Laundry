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
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError






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
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'error': 'Invalid password.'})


    return render(request, 'account/login.html')


def logout_view(request):
    logout(request)
    return redirect('home')


User = get_user_model()

@csrf_exempt
def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        phone_number = request.POST.get('phone_number', '')
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')

        # Basic form validation
        if not first_name or not last_name or not phone_number or not password1 or not password2:
            return JsonResponse({'success': False, 'error': 'All fields are required.'}, status=400)

        # Additional password validation
        if password1 != password2:
            return JsonResponse({'success': False, 'error': 'Passwords do not match.'}, status=400)

        # Custom phone number validation if needed
        # You can add your phone number validation logic here

        # Create the user if the validation passes
        User = get_user_model()
        try:
            user = User.objects.create_user(first_name=first_name, last_name=last_name, phone_number=phone_number, password=password1)
            return JsonResponse({'success': True})
        except ValidationError as e:
            return JsonResponse({'success': False, 'error': e.message}, status=400)

    # Return a bad request response if the request method is not POST
    return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=400)



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

@login_required
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



def check_phone_number(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number', None)
        
        if phone_number:
            try:
                # Check if the phone number already exists in the CustomUser model
                user = CustomUser.objects.get(phone_number=phone_number)
                user_exists = True
            except CustomUser.DoesNotExist:
                user_exists = False

            return JsonResponse({'number_exists': user_exists})
        else:
            return JsonResponse({'error': 'Phone number not provided.'})
    else:
        return JsonResponse({'error': 'Invalid request method.'})


