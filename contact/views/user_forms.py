from django.shortcuts import render, redirect
from django.contrib import messages
from contact.forms import RegisterForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth


def register(request):
    
    if request.method == 'GET':
        form = RegisterForm()
    
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        
        if form.is_valid():
            form.save()
            messages.success(
                request,
                'User registered',
            )
            return redirect('contact:index')
    
    context = {
        'form': form,
    }
    
    
    return render(
        request,
        'contact/register.html',
        context,
    )
    
    
def login_view(request):
    
    if request.method == 'GET':
        form = AuthenticationForm(request)
    
    if request.method == 'POST':
        form = AuthenticationForm(
            request, 
            data=request.POST
        )
        
        if form.is_valid():
            user = form.get_user()
            auth.login(request, user)
            messages.success(
                request,
                'Logged in',
            )
            return redirect('contact:index')
        else:
            messages.error(
                request,
                'Username or Password invalid',
            )
            
    context = {
        'form': form,
    }
    
    return render(  
        request,
        'contact/login.html',
        context,
    )
    
def logout_view(request):
    auth.logout(request)
    return redirect('contact:login')