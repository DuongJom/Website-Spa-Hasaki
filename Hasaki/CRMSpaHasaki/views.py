from django.shortcuts import render
 
def login_options(request):
    return render(request, 'login_options.html')

def phone_verify(request):
    return render(request, 'phone_verification.html')

def login(request):
    return render(request, 'login.html')