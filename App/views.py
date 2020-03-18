from django.shortcuts import render
from django.views.generic import ListView, DetailView, View
from django.contrib.auth.models import User, auth
from .models import UserProfile
# Create your views here.
def index(request):
    return render(request, "index.html")
# Create your views here.
def login(request):
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['userpassword']

        user = auth.authenticate(username=username, password=password)
        if (user is not None):
            auth.login(request, user)
            account_type = user.user_type
            if (account_type=="Student"):
                return redirect("dashboard2.html")
            elif (account_type=="Parent"):
                return redirect("dashboard5.html")
            elif (account_type=="Teacher"):
                return redirect("dashboard5.html")
            elif (account_type=="Admin"):
                return redirect("dashboard5.html")
            elif (account_type=="Liberian"):
                return redirect("dashboard5.html")
            elif (account_type=="Accountant"):
                return redirect("dashboard5.html")
            return render(request, 'auth-login.html', {"message": "The user does not exist"})

        else:
            return render(request, 'auth-login.html', {"message": "The user does not exist"})
    else:
        return render(request, 'auth-login.html')
def validate(request):
        if request.method=='POST':
            secrete_key = request.POST['secrete_pin']
            key = user.objects.all().filter(usertype="Student").secret_pin
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
