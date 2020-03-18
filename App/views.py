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
        password = request.POST['pass']
        cat = request.POST['cat']

        user = auth.authenticate(username=username, password=password, cat=cat)
        if (user is not None) and (cat=="Student"):
            auth.login(request, user)
            return redirect("dashboard2.html")
        elif (user is not None) and (cat=="Teacher"):
            auth.login(request, user)
            return redirect("dashboard4.html")
        elif (user is not None) and (cat=="Parent"):
            auth.login(request, user)
            return redirect("dashboard5.html")
        else:
            return render(request, 'auth-login.html', {"message": "The user does not exist"})
    else:
        return render(request, 'auth-login.html')

def recover(request):
    return render(request, "auth-recoverpw.html")
def verify(request):
    return render(request, "auth-lock-screen.html")
