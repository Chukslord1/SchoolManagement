from django.shortcuts import render,redirect
from django.views.generic import ListView, DetailView, View
from django.contrib.auth.models import User, auth
from .models import UserProfile, UnusedPins, UsedPins, BulkStudent
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
    context = {"parents":UserProfile.objects.all().filter(user_type="Parent")}
    if request.method == 'POST':
        if request.POST.get('form_type')=="addstudent":
            name = request.POST['name']
            username= request.POST['username']
            parent = request.POST['parent']
            class_room = request.POST['class_room']
            section = request.POST['section']
            gender = request.POST['gender']
            school_type = request.POST['school_type']
            birthday = request.POST['birthday']
            phone_number = request.POST['phone_number']
            address = request.POST['address']
            image = request.POST['image']


            email = request.POST['email']
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            UserProfile_id=username

            if password1==password2:
                if User.objects.filter(email=email).exists():
                        return render(request, 'add-student.html', {"message": "The user is already registered"}, context)
                else:
                    user = User.objects.create(username=username, password=password1, email=email )
                    user.set_password(user.password)
                    user.save()
                    profile = UserProfile.objects.create(user=user, name=name, user_type='Student', parent=parent, class_room=class_room, section=section, gender=gender, school_type=school_type, birthday=birthday, phone_number=phone_number, address=address, image=image)
                    profile.save()
                    return redirect('add-student.html', {"message": "Student Added"}, context)
            else:
                return render(request, 'add-student.html', {"message": "The passwords don't match"}, context)
        elif request.POST.get('form_type')=="bulkstudent":
            name = request.POST['name']
            parent = request.POST['parent']
            class_room = request.POST['class_room']
            session = request.POST['session']
            gender = request.POST['gender']

            email = request.POST['email']
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            BulkStudent_id=name

            if password1==password2:
                if User.objects.filter(email=email).exists():
                     return render(request, "add-student.html", {"message": "The user is already registered"})
                else:
                    profile = BulkStudent.objects.create(name=name, parent=parent, class_room=class_room, session=session, gender=gender, email=email, password=password1)
                    profile.set_password(profile.password)
                    profile.save()
                    return render(request, "add-student.html", {"message": "Student Added"}, context)
            else:
                return render(request, "add-student.html", {"message": "The passwords don't match"}, context)

        elif request.POST.get("form_type")=="csv":
            class_room = request.POST['class_room']
            session = request.POST['session']
        else:
            return render(request, "add-student.html", context)
    else:
        return render(request, "add-student.html", context)


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
    context = {"teachers":UserProfile.objects.all().filter(user_type="Teacher")}
    if request.method == 'POST':
        if request.POST.get('form_type')=="create":
            name = request.POST['name']
            username= request.POST['username']
            gender = request.POST['gender']
            birthday = request.POST['birthday']
            phone_number = request.POST['phone_number']
            address = request.POST['address']
            image = request.POST['image']


            email = request.POST['email']
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            UserProfile_id=username

            if password1==password2:
                if User.objects.filter(email=email).exists():
                        return render(request, 'manage-teacher.html', {"message": "The user is already registered"})
                else:
                    user = User.objects.create(username=username, password=password1, email=email )
                    user.set_password(user.password)
                    user.save()
                    profile = UserProfile.objects.create(user=user, name=name, user_type='Accountant', gender=gender,birthday=birthday, phone_number=phone_number, address=address, image=image)
                    profile.save()
                    return render(request, 'manage-teacher.html', {"message": "Student Added"}, context)
            else:
                return render(request, 'manage-teacher.html', {"message": "The passwords don't match"}, context)
        elif request.POST.get('form_type')=="edit":
            user.profile.name = request.POST['name']
            user.profile.username = request.POST['username']
            user.profile.gender = request.POST['gender']
            user.profile.address = request.POST['address']

            user.profile.email = request.POST['email']
            email= user.profile.email
            user.profile.password = request.POST['passoword']
            profile.set_password(profile.password)
            if User.objects.filter(email=email).exists():
                return render(request, "manage-teacher.html", {"message": "The user is already registered"}, context)
            else:
                user.profile.save()
        else:
            return render(request, "manage-teacher.html", context)
    else:
        return render(request, "manage-teacher.html", context)


def manageStudent(request):
    return render(request, "manage-student.html")

def manageParent(request):
    context = {"parents":UserProfile.objects.all().filter(user_type="Parent")}
    if request.method == 'POST':
        if request.POST.get('form_type')=="create":
            name = request.POST['name']
            username= request.POST['username']
            gender = request.POST['gender']
            birthday = request.POST['birthday']
            phone_number = request.POST['phone_number']
            address = request.POST['address']
            image = request.POST['image']


            email = request.POST['email']
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            UserProfile_id=username

            if password1==password2:
                if User.objects.filter(email=email).exists():
                        return render(request, 'manage-parent.html', {"message": "The user is already registered"})
                else:
                    user = User.objects.create(username=username, password=password1, email=email )
                    user.set_password(user.password)
                    user.save()
                    profile = UserProfile.objects.create(user=user, name=name, user_type='Accountant', gender=gender,birthday=birthday, phone_number=phone_number, address=address, image=image)
                    profile.save()
                    return render(request, 'manage-parent.html', {"message": "Student Added"}, context)
            else:
                return render(request, 'manage-parent.html', {"message": "The passwords don't match"}, context)
        elif request.POST.get('form_type')=="edit":
            user.profile.name = request.POST['name']
            user.profile.username = request.POST['username']
            user.profile.gender = request.POST['gender']
            user.profile.address = request.POST['address']

            user.profile.email = request.POST['email']
            email= user.profile.email
            user.profile.password = request.POST['passoword']
            profile.set_password(profile.password)
            if User.objects.filter(email=email).exists():
                return render(request, "manage-parent.html", {"message": "The user is already registered"}, context)
            else:
                user.profile.save()
        else:
            return render(request, "manage-parent.html", context)
    else:
        return render(request, "manage-parent.html", context)


def manageLibarian(request):
    context = {"libarians":UserProfile.objects.all().filter(user_type="Liberian")}
    if request.method == 'POST':
        if request.POST.get('form_type')=="create":
            name = request.POST['name']
            username= request.POST['username']
            gender = request.POST['gender']
            birthday = request.POST['birthday']
            phone_number = request.POST['phone_number']
            address = request.POST['address']
            image = request.POST['image']


            email = request.POST['email']
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            UserProfile_id=username

            if password1==password2:
                if User.objects.filter(email=email).exists():
                        return render(request, 'manage-libarian.html', {"message": "The user is already registered"})
                else:
                    user = User.objects.create(username=username, password=password1, email=email )
                    user.set_password(user.password)
                    user.save()
                    profile = UserProfile.objects.create(user=user, name=name, user_type='Accountant', gender=gender,birthday=birthday, phone_number=phone_number, address=address, image=image)
                    profile.save()
                    return render(request, 'manage-libarian.html', {"message": "Student Added"}, context)
            else:
                return render(request, 'manage-libarian.html', {"message": "The passwords don't match"}, context)
        elif request.POST.get('form_type')=="edit":
            user.profile.name = request.POST['name']
            user.profile.username = request.POST['username']
            user.profile.gender = request.POST['gender']
            user.profile.address = request.POST['address']

            user.profile.email = request.POST['email']
            email= user.profile.email
            user.profile.password = request.POST['passoword']
            profile.set_password(profile.password)
            if User.objects.filter(email=email).exists():
                return render(request, "manage-libarian.html", {"message": "The user is already registered"}, context)
            else:
                user.profile.save()
        else:
            return render(request, "manage-libarian.html", context)
    else:
        return render(request, "manage-libarian.html", context)


def manageAdmin(request):
    context = {"admins":UserProfile.objects.all().filter(user_type="Admin")}
    if request.method == 'POST':
        if request.POST.get('form_type')=="create":
            name = request.POST['name']
            username= request.POST['username']
            gender = request.POST['gender']
            birthday = request.POST['birthday']
            phone_number = request.POST['phone_number']
            address = request.POST['address']
            image = request.POST['image']


            email = request.POST['email']
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            UserProfile_id=username

            if password1==password2:
                if User.objects.filter(email=email).exists():
                        return render(request, 'manage-admin.html', {"message": "The user is already registered"})
                else:
                    user = User.objects.create(username=username, password=password1, email=email )
                    user.set_password(user.password)
                    user.save()
                    profile = UserProfile.objects.create(user=user, name=name, user_type='Accountant', gender=gender,birthday=birthday, phone_number=phone_number, address=address, image=image)
                    profile.save()
                    return render(request, 'manage-admin.html', {"message": "Student Added"}, context)
            else:
                return render(request, 'manage-admin.html', {"message": "The passwords don't match"}, context)
        elif request.POST.get('form_type')=="edit":
            user.profile.name = request.POST['name']
            user.profile.username = request.POST['username']
            user.profile.gender = request.POST['gender']
            user.profile.address = request.POST['address']

            user.profile.email = request.POST['email']
            email= user.profile.email
            user.profile.password = request.POST['passoword']
            profile.set_password(profile.password)
            if User.objects.filter(email=email).exists():
                return render(request, "manage-admin.html", {"message": "The user is already registered"}, context)
            else:
                user.profile.save()
        else:
            return render(request, "manage-admin.html", context)

    else:
        return render(request, "manage-admin.html", context)



def manageAccountant(request):
    context = {"accountants":UserProfile.objects.all().filter(user_type="Accountant")}
    if request.method == 'POST':
        if request.POST.get('form_type')=="create":
            name = request.POST['name']
            username= request.POST['username']
            gender = request.POST['gender']
            birthday = request.POST['birthday']
            phone_number = request.POST['phone_number']
            address = request.POST['address']
            image = request.POST['image']


            email = request.POST['email']
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            UserProfile_id=username

            if password1==password2:
                if User.objects.filter(email=email).exists():
                        return render(request, 'manage-accountant', {"message": "The user is already registered"})
                else:
                    user = User.objects.create(username=username, password=password1, email=email )
                    user.set_password(user.password)
                    user.save()
                    profile = UserProfile.objects.create(user=user, name=name, user_type='Accountant', gender=gender,birthday=birthday, phone_number=phone_number, address=address, image=image)
                    profile.save()
                    return render(request, 'manage-accountant.html', {"message": "Student Added"}, context)
            else:
                return render(request, 'manage-accountant.html', {"message": "The passwords don't match"}, context)
        elif request.POST.get('form_type')=="edit":
            user.profile.name = request.POST['name']
            user.profile.username = request.POST['username']
            user.profile.gender = request.POST['gender']
            user.profile.address = request.POST['address']

            user.profile.email = request.POST['email']
            email= user.profile.email
            user.profile.password = request.POST['passoword']
            profile.set_password(profile.password)
            if User.objects.filter(email=email).exists():
                return render(request, "manage-accountant.html", {"message": "The user is already registered"}, context)
            else:
                user.profile.save()
        else:
            return render(request, "manage-accountant.html", context)

    else:
        return render(request, "manage-accountant.html", context)


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
