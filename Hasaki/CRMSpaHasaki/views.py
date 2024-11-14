from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
 
def login_options(request):
    if request.method == 'GET':
        return render(request, 'login_options.html')

@csrf_protect
def phone_verify(request):
    if request.method == 'POST':
        return redirect('/reset-password')
    return render(request, 'phone_verification.html')

@csrf_protect
def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    return redirect("/login-options")

@csrf_protect
def reset_password(request):
    if request.method == 'GET':
        return render(request, 'new_password.html')
    return redirect('/')

def get_list_appointments(request):
    if request.method == 'GET':
        return render(request,'appointments.html')