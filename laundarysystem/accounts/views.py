from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .forms import SignUpForm
from django.contrib.auth import get_user_model
from django.conf import settings





# Create your views here.
def login_view(request):
    if request.user.is_authenticated:
            return redirect('dashboard:home')     
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard:home')  # Replace 'home' with the name of your homepage URL pattern
        else:
            messages.error(request, 'Invalid username or password.')
            #return redirect('account:login')  # Redirect back to the login page
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
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
            return redirect('account:login')
    else:
        form = SignUpForm()
    return render(request, 'account/register.html', {'form': form})