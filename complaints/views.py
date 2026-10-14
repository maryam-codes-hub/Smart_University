from django.shortcuts import render,redirect
from django.contrib import messages

def landing(request):
    return render(request,'landing.html')

def about(request):
    return render(request,'about.html')

def services(request):
    return render(request,'services.html')
def contact(request):
    context = {}

    if 'name' in request.POST:
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        context = {
            'submitted': True,
            'name': name,
            'email': email,
            'subject': subject,
            'message': message,
        }

        print(name, email, subject, message)
        messages.success(request, f'Thank you, {name}! We received your message and will reply to {email} soon.')
        return redirect('contact')

    return render(request, 'contact.html', context)


