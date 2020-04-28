from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import UserRegistrationForm
from django.contrib.auth.decorators import login_required
from django.urls import path
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def home(request):
    return render(request, 'account/home.html')


def login_view(request):
    return render(request, 'account/login.html', {})

def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully")
    return redirect('home')

def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        print(request.POST['psw'])
        print("form", form)
        username = form.cleaned_data.get('username')
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('musicServiceAuth')

        #if form.is_valid():
            #print("valid")
            #username = form.cleaned_data.get('username')
            #password = form.cleaned_data.get('password')
            #print("username--------", username)
            #user = authenticate(username=username, password=password)
            #print("user", user)



    print('MADE IT HERE')
    return render(request, 'account/login.html', {})

def register(request):
    print("Im here 1")
    if request.method == 'POST':
        print("Im here")
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            print("-------", form.cleaned_data['email'])
            email = form.cleaned_data.get('email')
            # this message appears on login page, needs to appear on lib (i think i fix this by using my template)
            # messages.success(request, f'Account created for {username}!')
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'account/register.html', {'form': form})
