from django.shortcuts import render,redirect
from django.contrib import messages

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

        print(name, email, message)

       
        return redirect('thankyou')

    return render(request, 'contact.html')

def thankyou(request):
    return render(request, 'thankyou.html')


