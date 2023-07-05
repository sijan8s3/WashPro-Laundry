from django.shortcuts import render

# Create your views here.

def home(request):
    context= {'user': request.user}
    return render(request=request, template_name='base/home.html', context=context)


#def login(request):
#    return render(request=request, template_name='base/login.html')


def register(request):
    return render(request=request, template_name='base/register.html')

