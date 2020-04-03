from django.shortcuts import render,redirect
from django.views.generic import ListView, DetailView, View
from django.contrib.auth.models import User, auth
from .models import UserProfile, UnusedPins, UsedPins
from django.contrib.auth.decorators import login_required
import random
import string

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
        secret_key = (request.POST['secret_pin'])
        user=request.user
        if UnusedPins.objects.filter(pin=secret_key):
            if not UsedPins.objects.filter(pin=secret_key):
                profile = user.profile
                profile.secret_pin = secret_key
                profile.save()
                special = UsedPins.objects.create(pin=secret_key)
                special.save()
                key = UnusedPins.objects.filter(pin=secret_key)
                key.delete()
                return render(request, "index.html")

        else:
        	if UsedPins.objects.filter(pin=secret_key):
        		#User has used the key before
        		return render(request, "index.html")
        	else:
        		#user doesnt have a key, hes probably forging or putting a pin incorrectly
        		return "Please input a valid pin"
    else:
        return render(request, 'auth-lock-screen.html')
@login_required
def logout(request):
    auth.logout(request)
    return redirect("auth-login.html")



def randomStringDigits(stringLength=6):
    """Generate a random string of letters and digits """
    lettersAndDigits = string.ascii_letters + string.digits
    return ''.join(random.choice(lettersAndDigits) for i in range(stringLength))

def generate(request):
    params = {"pins":UnusedPins.objects.all()}
    if request.method == 'POST':
        number = request.POST['number']
        x = int(number)
        for i in range(x):
            code = UnusedPins.objects.create(pin=randomStringDigits(12))
            code.save()
            print (randomStringDigits(12))
        return render(request,"gen.html",params)
    else:
        return render(request,"gen.html")
#so create a database for used and unused and delete used ones from unused and add to used and assign the current used to user
def addStudent(request):
    return render(request, "add-student.html")

def Student(request):
    return render(request, "student.html")
def timeTable(request):
    return render(request, "time-table.html")

def syllabus(request):
    return render(request, "syllabus.html")

def subject(request):
    return render(request, "subject.html")

def sms(request):
    return render(request, "sms.html")

def profile(request):
    return render(request, "profile.html")

def manageTeacher(request):
    return render(request, "manage-teacher.html")

def manageStudent(request):
    return render(request, "manage-student.html")

def manageParent(request):
    return render(request, "manage-parent.html")

def manageLibarian(request):
    return render(request, "manage-libarian.html")

def manageAdmin(request):
    return render(request, "manage-admin.html")

def manageAccountant(request):
    return render(request, "manage-accountant.html")

def Dept(request):
    return render(request, "department.html")

def Attend(request):
    return render(request, "daily-attendance.html")

def Class(request):
    return render(request, "class.html")

def Chat(request):
    return render(request, "chat.html")

def Calendar(request):
    return render(request, "calendar.html")

def Admission(request):
    return render(request, "admission.html")
