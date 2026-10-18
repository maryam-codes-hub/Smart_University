from django.shortcuts import render,redirect
from django.contrib import messages
from .models import ContactMessage
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import ContactMessage, Complaint
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test

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


@login_required
def give_feedback(request):
    complaints = Complaint.objects.filter(
        student=request.user,
        status='resolved',
        feedback__isnull=True,
    )
    return render(request, 'give_feedback.html', {'complaints': complaints})


def choose_portal(request):
    return render(request, 'choose_portal.html')


def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_staff:
            login(request, user)
            return redirect('admin_dashboard')

        messages.error(request, 'Invalid credentials or not an admin account.')
        return redirect('admin_login')

    return render(request, 'admin_login.html')


def is_admin(user):
    return user.is_authenticated and user.is_staff


@user_passes_test(is_admin, login_url='admin_login')
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')


@user_passes_test(is_admin, login_url='admin_login')
def admin_dashboard(request):
    context = {
        'total': Complaint.objects.count(),
        'pending': Complaint.objects.filter(status='pending').count(),
        'in_progress': Complaint.objects.filter(status='in_progress').count(),
        'resolved': Complaint.objects.filter(status='resolved').count(),
    }
    return render(request, 'admin_dashboard.html', context)

@user_passes_test(is_admin, login_url='admin_login')
def admin_complaints(request):
    complaints = Complaint.objects.select_related('student').order_by('-submission_date')

    status = request.GET.get('status')
    if status:
        complaints = complaints.filter(status=status)

    return render(request, 'admin_complaints.html', {
        'complaints': complaints,
        'current': status,
        'status_choices': Complaint.STATUS_CHOICES,
    }) 
@user_passes_test(is_admin, login_url='admin_login')
def update_status(request, pk):
    if request.method == 'POST':
        complaint = get_object_or_404(Complaint, pk=pk)
        new_status = request.POST.get('status')

        allowed = [value for value, label in Complaint.STATUS_CHOICES]

        if new_status in allowed:
            complaint.status = new_status
            complaint.save()
            messages.success(request, f'Complaint #CMP-{complaint.id:04d} marked as {complaint.get_status_display()}.')
        else:
            messages.error(request, 'Invalid status.')

    return redirect('admin_complaints')