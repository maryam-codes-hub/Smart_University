from django.shortcuts import render,redirect
from django.contrib import messages
from .models import ContactMessage
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def landing(request):
    return render(request,'landing.html')

def about(request):
    return render(request,'about.html')

def services(request):
    return render(request,'services.html')
def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        
        message = request.POST.get('message')

        # print(name, email, message)
        ContactMessage.objects.create(name=name, email=email, message=message)

       
        return redirect('thankyou')

    return render(request, 'contact.html')

def thankyou(request):
    return render(request, 'thankyou.html')


def student_register(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password')
        confirm = request.POST.get('confirm_password')

        if password != confirm:
            messages.error(request, 'Passwords do not match.')
            return redirect('student_register')

        if len(password) < 8:
            messages.error(request, 'Password must be at least 8 characters.')
            return redirect('student_register')

        if User.objects.filter(username=email).exists():
            messages.error(request, 'An account with this email already exists.')
            return redirect('student_register')

        User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=name,
        )

        messages.success(request, 'Account created! Please login.')
        return redirect('student_login')

    return render(request, 'student_register.html')

def student_login(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('student_dashboard')

        messages.error(request, 'Invalid email or password.')
        return redirect('student_login')

    return render(request, 'student_login.html')
@login_required
def student_dashboard(request):
    return render(request, 'student_dashboard.html')


def student_logout(request):
    if request.method == 'POST':
        logout(request)
    return redirect('landing')


