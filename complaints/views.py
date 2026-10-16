from django.shortcuts import render,redirect
from django.contrib import messages
from .models import ContactMessage
from django.contrib.auth.models import User

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

        messages.success(request, 'Account created successfully!')
        return redirect('student_register')

    return render(request, 'student_register.html')


