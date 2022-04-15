from django.shortcuts import render,redirect
from .models import CustomUser
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .forms import UserRegistrationForm
from manager.models import AdvanceBooking


def loginPage(request):

    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        user = authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            if request.user.is_manager:
                return redirect('manager')
            elif request.user.is_customer:
                return redirect('client')
            else:
                return redirect('home')
        else:
            messages.error(request,"Username or Password does not match")
    context={'page':page}
    return render(request,'account/login_registration.html',context)

def ManagerSignUpView(request):
    page = 'manager'
    form = UserRegistrationForm()
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # to reformat user input
            user = form.save(commit=False)
            # saving all username in lower case format
            user.username = user.username.lower()
            user.is_manager=True
            user.save()
            adv = AdvanceBooking.objects.create(manager_id=CustomUser.objects.get(id=user.id))
            login(request,user)
            return redirect('manager')
        else:
            messages.error(request,f"An error occured")

    context = {'page':page,'form':form}

    return render(request,'account/login_registration.html',context)

def CustomerSignUpView(request):
    page = 'customer'
    form = UserRegistrationForm()
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # to reformat user input
            user = form.save(commit=False)

            # saving all username in lower case format
            user.username = user.username.lower()
            user.is_customer = True
            user.save()
            login(request,user)
            return redirect('client')
        else:
            messages.error(request,f"An error occured")

    context = {'page':page,'form':form}

    return render(request,'account/login_registration.html',context)


def logoutPage(request):
    logout(request)
    return redirect('home')


