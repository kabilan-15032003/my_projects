from django.shortcuts import render, redirect
from django.contrib.auth.models import User
import registeration.models
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
# Create your views here.

def signup(request):

    if request.method == 'POST':
        username = str(request.POST['username'])
        username.lower()

        # To handle the username with spaces
        if ' ' in username:
            messages.error(request, 'Do not use spaces in the username')
            return redirect('/accounts/signup')

        first_name = request.POST['fname']
        last_name = request.POST['lname']
        email_id = request.POST['email']
        mobile_number = request.POST['num']
        dob = request.POST['dob']
        pass1 = request.POST['password1']
        pass2 = request.POST['password2']

        # To handle the only when all conditions satisfied like unique username, both passwords matching
        if pass1 == pass2 and not(User.objects.filter(username=username).exists()):
            user1 = User.objects.create_user(username=username, email=email_id, password=pass1, first_name=first_name, last_name=last_name)
            user1.save()
            print('User created successfully')
            user2 = registeration.models.UserProfile.objects.create(user=user1, first_name=first_name, last_name=last_name, phone_number=mobile_number, date_of_birth=dob)
            user2.save()
            messages.success(request, 'Account created successfully')
            return redirect('/accounts/signin')

        else:

            # When password1 not matching with password2
            if pass1 != pass2:
                messages.error(request, 'Passwords are not matching')
                return redirect('/accounts/signup')

            # When username is already exists
            elif User.objects.filter(username=username).exists():
                messages.error(request, 'Username already taken')
                return redirect('/accounts/signup')

    return render(request, 'signup.html')


def signin(request):

    if request.method == 'POST':
        user = request.POST['Username']
        password = request.POST['Password']

        user = authenticate(username=user, password=password)

        # When correct credentials entered by the user
        if user is not None:
            login(request, user)
            return redirect('/')

        # When username is correct and password was wrong
        elif User.objects.filter(username=user).exists():
            messages.error(request, 'Entered Wrong password')
            return redirect('/accounts/signin')

        # When the username itself wrong
        else:
            messages.error(request, 'Entered username not found')
            return redirect('/accounts/signin')

    return render(request, 'signin.html')


def signout(request):
    logout(request)
    return redirect('/')
