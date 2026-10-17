from django.shortcuts import render,redirect
from django.contrib import messages
from .models import ContactMessage
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import ContactMessage, Complaint
from django.shortcuts import render, redirect, get_object_or_404

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
    my_complaints = Complaint.objects.filter(student=request.user)

    context = {
        'total': my_complaints.count(),
        'in_progress': my_complaints.filter(status='in_progress').count(),
        'resolved': my_complaints.filter(status='resolved').count(),
    }

    return render(request, 'student_dashboard.html', context)


def student_logout(request):
    if request.method == 'POST':
        logout(request)
    return redirect('landing')


@login_required
def submit_complaint(request):
    if request.method == 'POST':
        title = request.POST.get('title').strip()
        description = request.POST.get('description').strip()
        if not title or not description:
            messages.error(request, 'Please fill in both title and description.')
            return redirect('submit_complaint')

        if len(title) > 200:
            messages.error(request, 'Title must be 200 characters or less.')
            return redirect('submit_complaint')
        

        Complaint.objects.create(
            student=request.user,
            title=title,
            description=description,
        )
           
        messages.success(request, 'Complaint submitted successfully! Status: Pending.')
        return redirect('student_dashboard')


    return render(request, 'submit_complaint.html')

@login_required
def track_status(request):
    complaints = Complaint.objects.filter(student=request.user).order_by('-submission_date')
    return render(request, 'track_status.html', {'complaints': complaints})


@login_required
def complaint_detail(request, pk):
    complaint = get_object_or_404(Complaint, pk=pk, student=request.user)
    return render(request, 'complaint_detail.html', {'complaint': complaint})