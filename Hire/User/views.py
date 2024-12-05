from django.contrib import messages
from django.shortcuts import redirect, render,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout

# Create your views here.


def index(request):
    return render(request, "index.html")


def register(request):
    if request.method == 'POST':
        uname=request.POST.get("name")
        email=request.POST.get("email")
        pass1=request.POST.get("password")
        pass2=request.POST.get("c_password")
        phone=request.POST.get("phone")

        if User.objects.filter(username=uname).exists(): 
            messages.error(request, 'Username already taken. Please choose a different one.')
        elif pass1!=pass2:
            messages.error(request, 'Your password and confirm password are not Same!!.')
        else:
            my_user=User.objects.create_user(uname,email,pass1)
            my_user.save()
            messages.success(request, 'Register Successfully')
        
    return render(request, "register.html")


def login(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('index')
        else:
            return HttpResponse ("Username or Password is incorrect!!!")

    return render (request,'base.html')


def contact(request):
    return render(request, "contact.html")


def my_resume(request):
    return render(request, "my_resume.html")


def applications(request):
    return render(request, "applications.html")


def job_details(request):
    return render(request, "job_details.html")


def jobs(request):
    return render(request, "jobs.html")


