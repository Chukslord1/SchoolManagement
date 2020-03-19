from django.shortcuts import render
from django.views.generic import ListView, DetailView, View
from django.contrib.auth.models import User, auth
from .models import UserProfile
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    return render(request, "index.html")
# Create your views here.
def login(request):
    account_type = UserProfile.objects.filter(user=request.user, user_type="user_type")
    if (request.method=='POST'):
        username = request.POST['username']
        password = request.POST['userpassword']
        user = auth.authenticate(username=username, password=password)
        account_type = UserProfile.objects.filter(user=request.user, user_type="user_type")
        if (user is not None):
            auth.login(request, user)
            account_type = UserProfile.objects.filter(user=request.user, user_type="user_type")
            print(account_type)
            return redirect("index.html")

        else:
            print(account_type)
            return render(request, 'auth-login.html', {"message": "The user does not exist"})
    else:
        print(account_type)
        return render(request, 'auth-login.html')

def validate(request):
        if request.method=='POST':
            secrete_key = request.POST['secrete_pin']
            key = UserProfile.objects.all().filter(user_type="Student").secret_pin
            if (secrete_key==key):
                return redirect("index.html")
            else:
                return redirect("auth-lock-screen.html")
        else:
            return render(request, 'auth-lock-screen.html')
def recover(request):
    return render(request, "auth-recoverpw.html")
def verify(request):
    return render(request, "auth-lock-screen.html")
