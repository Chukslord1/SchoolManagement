from django.shortcuts import render,redirect
from django.views.generic import ListView, DetailView, View
from django.contrib.auth.models import User, auth
from .models import UserProfile
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    global user_type
    user=request.user
    account_type = user.profile.user_type
    if (account_type=="Student"):
        return redirect("auth-lock-screen.html")
    elif(account_type=="Parent"):
        return render(request,"index.html")
    elif(account_type=="Teacher"):
        return render(request,"dashboard.html")
    elif(account_type=="Admin"):
        return render(request,"dashboard5.html")
    elif(account_type=="Liberian"):
        return render(request,"dashboard4.html")
    elif(account_type=="Accountant"):
        return render(request,"dashboard6.html")
    else:
        return render(request, 'auth-login.html')
# Create your views here.
def login(request):
    if (request.method=='POST'):
        username = request.POST['username']
        password = request.POST['userpassword']
        user = auth.authenticate(username=username, password=password)

        if (user is not None):
            auth.login(request, user)
            return redirect("index.html")

        else:

            return render(request, 'auth-login.html', {"message": "The user does not exist"})
    else:

        return render(request, 'auth-login.html')





def recover(request):
    return render(request, "auth-recoverpw.html")
def verify(request):
    if request.method=='POST':
        secret_key = int(request.POST['secret_pin'])

        user=request.user
        key = user.profile.secret_pin
        if (secret_key==key):
            return render(request, "index.html")
        else:
            return redirect("auth-lock-screen.html")
    else:
        return render(request, 'auth-lock-screen.html')
