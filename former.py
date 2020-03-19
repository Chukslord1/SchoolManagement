def login(request):
    account_type = UserProfile.objects.filter(user=request.user, user_type="user_type")
    if (request.method=='POST'):
        username = request.POST['username']
        password = request.POST['userpassword']
        user = auth.authenticate(username=username, password=password)
        if (user is not None):
            auth.login(request, user)
            if (UserProfile.objects.filter(user=request.user, user_type= "Student") is True):
                return redirect("index.html")
            elif (UserProfile.objects.filter(user=request.user, user_type= "Parent") is True):
                return redirect("dashboard5.html")
            elif (UserProfile.objects.filter(user=request.user, user_type= "Teacher") is True):
                return redirect("dashboard5.html")
            elif (UserProfile.objects.filter(user=request.user, user_type= "Admin") is True):
                return redirect("dashboard5.html")
            elif (UserProfile.objects.filter(user=request.user, user_type= "Liberian") is True):
                return redirect("dashboard5.html")
            elif (UserProfile.objects.filter(user=request.user, user_type= "Accountant") is True):
                return redirect("dashboard5.html")
            else:
                return render(request, 'auth-login.html', {"message": "The user does not have a userprofile"})

        else:

            return render(request, 'auth-login.html', {"message": "The user does not exist"})

    return render(request, 'auth-login.html')
