from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.core.paginator import Paginator
from datetime import datetime as dt, timedelta
from .models import Customer, Appointment, Service
from .helpers import get_appointment, read_data
 
def home(request):
    if request.method == "GET":
        return render(request,'../templates/home.html')
    
@csrf_protect
def appointment_booking(request):
    if request.method == "GET":
        services = Service.objects.all()
        context = {
            'isSuccess': False,
            'services': services
        }
        return render(request,'../templates/appointment_booking.html', {'context': context})
    
    # Check validity of fields on form
    customer_name = request.POST.get('name')
    phone = request.POST.get('phone')
    email = request.POST.get('email')
    note = request.POST.get('note')
    service = request.POST.get('service')
    appointment_date = request.POST.get('appointment_date')
    start_time = request.POST.get('start_time')
    end_time = dt.combine(dt.today(), dt.strptime(start_time, '%H:%M').time()) + timedelta(hours=1)

    if not customer_name or not phone or not email or not service or \
        not appointment_date or not start_time:
        return render(request, '../templates/appointment_booking.html', {'isSuccess': False})
    
    service_obj = Service.objects.filter(service_id=service).values()

    context = {
        'isSuccess': True,
        'customer_name': customer_name,
        'phone': phone,
        'email': email,
        'service': service_obj[0]['service_name'] if service_obj else "Không dịch vụ",
        'appointment_date': appointment_date,
        'note': note,
        'start_time': start_time,
        'end_time': f"{str(end_time.time().hour).zfill(2)}:{str(end_time.time().minute).zfill(2)}",
        'start_clock_type': "AM" if int(str(start_time).split(":")[0]) < 12 else "PM",
        'end_clock_type': "AM" if end_time.time().hour < 12 else "PM"
    }
    return render(request, '../templates/appointment_booking.html', {'context': context})

@csrf_protect
def phone_verify(request):
    if request.method == 'POST':
        return redirect('/reset-password')
    return render(request, '../templates/phone_verification.html')

@csrf_protect
def login(request):
    if request.method == 'GET':
        return render(request, '../templates/login.html')
    return redirect("/schedules")

@csrf_protect
def reset_password(request):
    if request.method == 'GET':
        return render(request, '../templates/new_password.html')
    return redirect('/')

def schedule(request):
    if request.method == 'GET':
        context = {
            'isShowModal': False,
            'data': get_appointment(),
            'dataModal': None
        }
        return render(request,'../templates/appointments.html', {"context": context})
    
def customers(request):
    if request.method == 'GET':
        lst_customers = read_data("Customers")
        for data in lst_customers:
            customer = Customer(customer_id=data['customer_id'],
                                customer_name=data['customer_name'],
                                phone_number=data['phone_number'],
                                email=data['email'],
                                created_date=data['created_date'],
                                is_delete=data['is_delete'])
            customer.save()
        customers = Customer.objects.all().values()
        paginator = Paginator(customers, 10)
        page_number = request.GET.get('page')
        if not page_number:
            page_number = 1
        
        customers_per_page = paginator.get_page(page_number)
        return render(request,'../templates/customers.html', {'customers': customers_per_page})
    
def show_detail_appointment(request, id):
    appointment = Appointment.objects.filter(appointment_id=id).values()
    context = {
        'isShowModal': True,
        'data': get_appointment(),
        'dataModal': appointment
    }
    return render(request,'../templates/appointment.html', {'context': context})
