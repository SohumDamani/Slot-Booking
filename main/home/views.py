from django.shortcuts import render,redirect

# Create your views here.

def home(request):
    try:
        a = request.user
        if a.is_manager:
            return redirect('manager')
        else:
            return redirect('client')
    except:
        return render(request,'home/home.html')