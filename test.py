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
