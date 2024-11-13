from django.shortcuts import render
 
def index(request):
    return render(request, 'index.html')

def phone_verify(request):
    return render(request, 'phone_verification.html')