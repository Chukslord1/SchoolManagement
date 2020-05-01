import os
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, View
from django.contrib.auth.models import User, auth
from .models import UserProfile, UnusedPins, UsedPins, BulkStudent, AttendClass
from django.contrib.auth.decorators import login_required
import random
import string
import xlwt
import requests
from django.http import HttpResponse
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet
import uuid
from SchoolManagement.settings import salt
import qrcode
from PIL import Image
from pyzbar.pyzbar import decode

def generate_fernet_key(master_key, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA512(),
        length=32,
        salt=salt.encode(),
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(master_key.encode()))
    return key.decode("utf-8")

def encrypt_text(text, key):
    encryptor = Fernet(key)
    hash = encryptor.encrypt(text.encode())
    return hash.decode()

key="adebowaleadeolu"
key= generate_fernet_key(key,salt)

@login_required
def index(request):
    items = ["stats"]
    stats = {
        "stats": {"students": UserProfile.objects.all().filter(user_type="Student").count(), "pins": UnusedPins.objects.all().count(), "teachers": UserProfile.objects.all().filter(user_type="Teacher").count(), "parents": UserProfile.objects.all().filter(user_type="Parent").count(), "staffs": UserProfile.objects.all().filter(user_type="Students").count()}

    }
    params = {"items": []}
    for item in items:
        new_params = stats[item]
        params["items"].append(new_params)
    global user_type
    user = request.user
    account_type = user.profile.user_type
    if (account_type == "Student"):
        return redirect("auth-lock-screen.html", params)
    elif(account_type == "Parent"):
        return render(request, "index.html", params)
    elif(account_type == "Teacher"):
        return render(request, "index.html", params)
    elif(account_type == "Admin"):
        if user.profile.session == "":
            user.profile.session = request.POST.get('session')
            user.profile.save()
        return render(request, "index1.html", params)
    elif(account_type == "Liberian"):
        return render(request, "index.html")
    elif(account_type == "Accountant"):
        return render(request, "index.html")
    else:
        return render(request, 'auth-login.html')


def login(request):
    if (request.method == 'POST'):
        username = request.POST['username']
        password = request.POST['userpassword']
        user = auth.authenticate(username=username, password=password)
        if (user is not None):
            auth.login(request, user)
            return redirect("index1.html")
        else:
            return render(request, 'auth-login.html', {"message": "The user does not exist"})
    else:
        return render(request, 'auth-login.html')


def recover(request):
    return render(request, "auth-recoverpw.html")


def verify(request):
    if request.method == 'POST':
        secret_key = (request.POST['secret_pin'])
        user = request.user
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
                # User has used the key before
                return render(request, "index.html")
            else:
                # user doesnt have a key, hes probably forging or putting a pin incorrectly
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
    params = {"pins": UnusedPins.objects.all()}
    if request.method == 'POST':
        number = request.POST['number']
        x = int(number)
        for i in range(x):
            code = UnusedPins.objects.create(pin=randomStringDigits(12))
            code.save()
            print(randomStringDigits(12))
        return render(request, "gen.html", params)
    else:
        return render(request, "gen.html")
# so create a database for used and unused and delete used ones from unused and add to used and assign the current used to user


def addStudent(request):
    account_type = UserProfile.objects.all().filter(user_type="Admin")
    account = account_type.values('session')
    context = {"parents": UserProfile.objects.all().filter(user_type="Parent")}
    if request.method == 'POST':
        if request.POST.get('form_type') == "addstudent":
            name = request.POST['name']
            username = request.POST['username']
            parent = request.POST['parent']
            class_room = request.POST['class_room']
            section = request.POST['section']
            gender = request.POST['gender']
            school_type = request.POST['school_type']
            birthday = request.POST['birthday']
            phone_number = request.POST['phone_number']
            address = request.POST['address']
            image = request.FILES['image']

            email = request.POST['email']
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            text= name
            detail=encrypt_text(text, key)

            UserProfile_id = username

            if password1 == password2:
                if User.objects.filter(email=email).exists():
                    return render(request, 'add-student.html', {"message": "The user is already registered"}, context)
                else:
                    user = User.objects.create(
                        username=username, password=password1, email=email)
                    user.set_password(user.password)
                    user.save()
                    m =qrcode.make(detail)
                    qrfilename="media\\" +name + "_qr.jpg"
                    m.save(qrfilename)
                    good='C:\\Users\\USER\\Desktop\\SchoolManagement\\' + qrfilename
                    profile = UserProfile.objects.create(user=user, name=name, user_type='Student', parent=parent, class_room=class_room, section=section,
                                                         gender=gender, school_type=school_type, birthday=birthday, phone_number=phone_number, address=address, image=image, qr_image=good)
                    profile.save()
                    new_image='http://advancescholar.com/media/' + str(image)
                    print(new_image)
                    r = requests.get("http://ec2-3-21-174-239.us-east-2.compute.amazonaws.com/save_user", params={
                        "name": name,
                        "image": new_image
                    }).json()
                    if r["success"]:
                        print("Saved Picture")
                    return redirect('add-student.html', {"message": "Student Added"}, context)
            else:
                return render(request, 'add-student.html', {"message": "The passwords don't match"}, context)
        elif request.POST.get('form_type') == "bulkstudent":
            name = request.POST.get('name', False)
            parent = request.POST.get('parent', False)
            gender = request.POST.get('gender', False)
            email = request.POST.get('email', False)
            password1 = request.POST.get('password1', False)
            password2 = request.POST.get('password2', False)
            BulkStudent_id = name

            if password1 == password2:
                if User.objects.filter(email=email).exists():
                    return render(request, "add-student.html", {"message": "The user is already registered"})
                else:
                    profile = BulkStudent.objects.create(
                        name=name, parent=parent, gender=gender, email=email, password=password1)
                    profile.save()
                    return redirect("add-student.html", {"message": "Student Added"}, context)
            else:
                return render(request, "add-student.html", {"message": "The passwords don't match"}, context)

        elif request.POST.get("form_type") == "csv":
            response = HttpResponse(content_type='application/ms-excel')
            response['Content-Disposition'] = 'attachment; filename="students.xls"'
            wb = xlwt.Workbook(encoding='utf-8')
            ws = wb.add_sheet('Students Data')
            row_num = 0
            font_style = xlwt.XFStyle()
            font_style.font.bold = True
            columns = ['Name', 'Username', 'Parent', 'Class', 'Section',
                       'Gender', 'School Type', 'Birthday', 'Phone Number', 'Address']
            for col_num in range(len(columns)):
                ws.write(row_num, col_num, columns[col_num], font_style)
            rows = UserProfile.objects.filter(user_type="Student").values_list(
                'user', 'name', 'parent', 'class_room', 'section', 'gender', 'school_type', 'birthday', 'phone_number', 'address')
            for row in rows:
                row_num += 1
                for col_num in range(len(row)):
                    ws.write(row_num, col_num, row[col_num], font_style)
            wb.save(response)
            return response
            return redirect("add-student.html", context)
        else:
            return render(request, "add-student.html", context)
    else:
        return render(request, "add-student.html", context)


def Student(request):
    context = {"students": UserProfile.objects.all().filter(
        user_type="Student")}
    if request.method == 'POST':
        previous_name = request.POST['previous_name']
        data = UserProfile.objects.get(name=previous_name)
        data.name = request.POST['name']
        data.username = request.POST['username']
        data.gender = request.POST['gender']
        data.address = request.POST['address']
        data.phone_number = request.POST['phone_number']

        data.email = request.POST['email']
        email = data.email
        if User.objects.filter(email=email).exists():
            return render(request, "student.html", {"message": "The user is already registered"}, context)
        else:
            data.save()
            return redirect("student.html", {"message": "Edited"}, context)
    return render(request, "student.html", context)


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
    account_type = UserProfile.objects.all().filter(user_type="Admin")
    account = account_type.values('session')
    context = {"teachers": UserProfile.objects.all().filter(
        user_type="Teacher")}
    if request.method == 'POST':
        if request.POST.get('form_type') == "create":
            name = request.POST['name']
            username = request.POST['username']
            gender = request.POST['gender']
            phone_number = request.POST['phone_number']
            address = request.POST['address']
            image = request.POST['image']

            email = request.POST['email']
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            UserProfile_id = username

            if password1 == password2:
                if User.objects.filter(email=email).exists():
                    return render(request, 'manage-teacher.html', {"message": "The user is already registered"})
                else:
                    user = User.objects.create(
                        username=username, password=password1, email=email)
                    user.set_password(user.password)
                    user.save()
                    profile = UserProfile.objects.create(
                        user=user, name=name, user_type='Teacher', gender=gender, phone_number=phone_number, address=address, image=image)
                    profile.save()
                    return redirect('manage-teacher.html', {"message": "Student Added"}, context)
            else:
                return render(request, 'manage-teacher.html', {"message": "The passwords don't match"}, context)
        elif request.POST.get('form_type') == "edit":
            previous_name = request.POST['previous_name']
            data = UserProfile.objects.get(name=previous_name)
            data.name = request.POST['name']
            data.username = request.POST['username']
            data.gender = request.POST['gender']
            data.address = request.POST['address']
            data.phone_number = request.POST['phone_number']

            data.email = request.POST['email']
            email = data.email
            if User.objects.filter(email=email).exists():
                return render(request, "manage-teacher.html", {"message": "The user is already registered"}, context)
            else:
                data.save()
                return redirect("manage-teacher.html", {"message": "Edited"}, context)
        else:
            return redirect("manage-teacher.html", context)
    else:
        return render(request, "manage-teacher.html", context)


def manageStudent(request):
    return render(request, "manage-student.html")


def manageParent(request):
    account_type = UserProfile.objects.all().filter(user_type="Admin")
    account = account_type.values('session')
    context = {"parents": UserProfile.objects.all().filter(user_type="Parent")}
    if request.method == 'POST':
        if request.POST.get('form_type') == "create":
            name = request.POST['name']
            username = request.POST['username']
            gender = request.POST['gender']
            phone_number = request.POST['phone_number']
            address = request.POST['address']
            image = request.POST['image']

            email = request.POST['email']
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            UserProfile_id = username

            if password1 == password2:
                if User.objects.filter(email=email).exists():
                    return render(request, 'manage-parent.html', {"message": "The user is already registered"})
                else:
                    user = User.objects.create(
                        username=username, password=password1, email=email)
                    user.set_password(user.password)
                    user.save()
                    profile = UserProfile.objects.create(
                        user=user, name=name, user_type='Parent', gender=gender, phone_number=phone_number, address=address, image=image)
                    profile.save()
                    return redirect('manage-parent.html', {"message": "Student Added"}, context)
            else:
                return render(request, 'manage-parent.html', {"message": "The passwords don't match"}, context)
        elif request.POST.get('form_type') == "edit":
            previous_name = request.POST['previous_name']
            data = UserProfile.objects.get(name=previous_name)
            data.name = request.POST['name']
            data.username = request.POST['username']
            data.gender = request.POST['gender']
            data.address = request.POST['address']
            data.phone_number = request.POST['phone_number']

            data.email = request.POST['email']
            email = data.email
            if User.objects.filter(email=email).exists():
                return render(request, "manage-parent.html", {"message": "The user is already registered"}, context)
            else:
                data.save()
                return redirect("manage-parent.html", {"message": "Edited"}, context)
        else:
            return redirect("manage-parent.html", context)
    else:
        return render(request, "manage-parent.html", context)


def manageLibarian(request):
    account_type = UserProfile.objects.all().filter(user_type="Admin")
    account = account_type.values('session')
    context = {"libarians": UserProfile.objects.all().filter(
        user_type="Liberian")}
    if request.method == 'POST':
        if request.POST.get('form_type') == "create":
            name = request.POST['name']
            username = request.POST['username']
            gender = request.POST['gender']
            phone_number = request.POST['phone_number']
            address = request.POST['address']
            image = request.POST['image']

            email = request.POST['email']
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            UserProfile_id = username

            if password1 == password2:
                if User.objects.filter(email=email).exists():
                    return render(request, 'manage-libarian.html', {"message": "The user is already registered"})
                else:
                    user = User.objects.create(
                        username=username, password=password1, email=email)
                    user.set_password(user.password)
                    user.save()
                    profile = UserProfile.objects.create(
                        user=user, name=name, user_type='Liberian', gender=gender, phone_number=phone_number, address=address, image=image)
                    profile.save()
                    return redirect('manage-libarian.html', {"message": "Student Added"}, context)
            else:
                return render(request, 'manage-libarian.html', {"message": "The passwords don't match"}, context)
        elif request.POST.get('form_type') == "edit":
            previous_name = request.POST['previous_name']
            data = UserProfile.objects.get(name=previous_name)
            data.name = request.POST['name']
            data.username = request.POST['username']
            data.gender = request.POST['gender']
            data.address = request.POST['address']
            data.phone_number = request.POST['phone_number']

            data.email = request.POST['email']
            email = data.email
            if User.objects.filter(email=email).exists():
                return redirect("manage-libarian.html", {"message": "The user is already registered"}, context)
            else:
                data.save()
                return redirect("manage-libarian.html", {"message": "Edited"}, context)
        else:
            return render(request, "manage-libarian.html", context)
    else:
        return render(request, "manage-libarian.html", context)


def manageAdmin(request):
    context = {"admins": UserProfile.objects.all().filter(user_type="Admin")}
    if request.method == 'POST':
        if request.POST.get('form_type') == "create":
            name = request.POST['name']
            username = request.POST['username']
            gender = request.POST['gender']
            phone_number = request.POST['phone_number']
            address = request.POST['address']
            image = request.POST['image']

            email = request.POST['email']
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            UserProfile_id = username

            if password1 == password2:
                if User.objects.filter(email=email).exists():
                    return render(request, 'manage-admin.html', {"message": "The user is already registered"})
                else:
                    user = User.objects.create(
                        username=username, password=password1, email=email)
                    user.set_password(user.password)
                    user.save()
                    profile = UserProfile.objects.create(
                        user=user, name=name, user_type='Admin', gender=gender, phone_number=phone_number, address=address, image=image)
                    profile.save()
                    return redirect('manage-admin.html', {"message": "Admin Added"}, context)
            else:
                return render(request, 'manage-admin.html', {"message": "The passwords don't match"}, context)
        elif request.POST.get('form_type') == "edit":
            user.profile.name = request.POST['name']
            user.profile.username = request.POST['username']
            user.profile.gender = request.POST['gender']
            user.profile.address = request.POST['address']
            user.profile.phone_number = request.POST['phone_number']

            user.profile.email = request.POST['email']
            email = user.profile.email
            if User.objects.filter(email=email).exists():
                return render(request, "manage-admin.html", {"message": "The user is already registered"}, context)
            else:
                user.profile.save()
                return redirect("manage-admin.html", {"message": "Edited"}, context)
        else:
            return redirect("manage-admin.html", context)

    else:
        return render(request, "manage-admin.html", context)


def manageAccountant(request):
    account_type = UserProfile.objects.all().filter(user_type="Admin")
    account = account_type.values('session')
    context = {"accountants": UserProfile.objects.all().filter(
        user_type="Accountant")}
    if request.method == 'POST':
        if request.POST.get('form_type') == "create":
            name = request.POST['name']
            username = request.POST['username']
            gender = request.POST['gender']
            phone_number = request.POST['phone_number']
            address = request.POST['address']
            image = request.POST['image']

            email = request.POST['email']
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            UserProfile_id = username

            if password1 == password2:
                if User.objects.filter(email=email).exists():
                    return render(request, 'manage-accountant.html', {"message": "The user is already registered"})
                else:
                    user = User.objects.create(
                        username=username, password=password1, email=email)
                    user.set_password(user.password)
                    user.save()
                    profile = UserProfile.objects.create(
                        user=user, name=name, user_type='Accountant', gender=gender, phone_number=phone_number, address=address, image=image)
                    profile.save()
                    return render(request, 'manage-accountant.html', context)
            else:
                return render(request, 'manage-accountant.html', context)
        elif request.POST.get('form_type') == "edit":
            previous_name = request.POST['previous_name']
            data = UserProfile.objects.get(name=previous_name)
            data.name = request.POST['name']
            data.username = request.POST['username']
            data.gender = request.POST['gender']
            data.address = request.POST['address']
            data.phone_number = request.POST['phone_number']

            data.email = request.POST['email']
            email = data.email
            if User.objects.filter(email=email).exists():
                return render(request, "manage-accountant.html", {"message": "The user is already registered"}, context)
            else:
                data.save()
                return redirect("manage-accountant.html", {"message": "Edited"}, context)
        else:
            return redirect("manage-accountant.html", context)

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


def test_attend(request):
    context = {"pics": AttendClass.objects.all()}
    if request.method == "POST":
        # This is your base64 string image
        image = request.FILES.get('snapshot')
        attend = AttendClass.objects.create(image=image)
        attend.save()
        r = requests.get("http://ec2-3-21-174-239.us-east-2.compute.amazonaws.com/match_user", params={
            "image": image
        }).json()
        if r["success"]:
            name = r["name"]
        return redirect("test_attend.html",{"message": "The user is already registered"+ name})
    return render(request, "test_attend.html", context)


def decrypt_text(hash, key):
    decryptor = Fernet(key)
    text = decryptor.decrypt(hash.encode())
    return text.decode("utf-8")

def decode_qr(request):
    if request.method=="POST":
        image=request.FILES['snapshot']
        data = decode(Image.open(image))
        first_result = data[0].data.decode("utf-8")
        second_result=decrypt_text(first_result,key)
        valid = UserProfile.objects.all().filter(name=second_result, user_type="Student").values_list('name')[0][0]
        if second_result==valid:
            return render(request,"qr_code.html", {"message": second_result + "is a registered student"})
        else:
            return redirect("qr_code.html", {"message": "Not a registered student"})
    return render(request, "qr_code.html")
