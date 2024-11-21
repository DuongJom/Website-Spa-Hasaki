from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.core.paginator import Paginator
from datetime import datetime as dt, timedelta
import datetime
from .models import Customer, Appointment
 
def home(request):
    if request.method == "GET":
        return render(request,'../templates/home.html')
    
def appointment_booking(request):
    if request.method == "GET":
        return render(request,'../templates/appointment_booking.html')
    
def login_options(request):
    if request.method == 'GET':
        return render(request, '../templates/login_options.html')

@csrf_protect
def phone_verify(request):
    if request.method == 'POST':
        return redirect('/reset-password')
    return render(request, '../templates/phone_verification.html')

@csrf_protect
def login(request):
    if request.method == 'GET':
        return render(request, '../templates/login.html')
    return redirect("/login-options")

@csrf_protect
def reset_password(request):
    if request.method == 'GET':
        return render(request, '../templates/new_password.html')
    return redirect('/')

def schedule(request):
    if request.method == 'GET':
        appointments = [
            {
                "appointment": Appointment(start_time=dt.now(), 
                        end_time=(dt.now() + timedelta(minutes=30)),
                        status=1),
                "customer_name": "Customer A",
                "phone":"0987654321"
            },
            {
                "appointment": Appointment(start_time=dt.now() + timedelta(minutes=30), 
                        end_time=(dt.now() + timedelta(minutes=60)),
                        status=0),
                "customer_name": "Customer B",
                "phone":"0975312468"
            },
            {
                "appointment": Appointment(start_time=dt.now() + timedelta(minutes=60), 
                        end_time=(dt.now() + timedelta(minutes=90)),
                        status=2),
                "customer_name": "Customer C",
                "phone":"0864213579"
            }
        ]

        times = [i for i in range(9,21)]
        data = dict()
        for t in times:
            key = datetime.time(hour=t).strftime("%H:%M")
            data[key] = []
            for appointment in appointments:
                if appointment['appointment'].start_time.hour == t:
                    data[key].append(appointment)
        return render(request,'../templates/appointments.html', {"data": data})
    
def customers(request):
    if request.method == 'GET':
        customers = [
            Customer(customer_id="001", customer_name="My My", created_date="27.03.2023",phone_number="0994511234"),
            Customer(customer_id="002", customer_name="Hải Yến", created_date="27.03.2023",phone_number="0987654321"),
            Customer(customer_id="003", customer_name="My My", created_date="27.03.2023",phone_number="0994511234"),
            Customer(customer_id="004", customer_name="Hải Yến", created_date="27.03.2023",phone_number="0987654321"),
            Customer(customer_id="005", customer_name="My My", created_date="27.03.2023",phone_number="0994511234"),
            Customer(customer_id="006", customer_name="Hải Yến", created_date="27.03.2023",phone_number="0987654321"),
            Customer(customer_id="007", customer_name="My My", created_date="27.03.2023",phone_number="0994511234"),
            Customer(customer_id="008", customer_name="Hải Yến", created_date="27.03.2023",phone_number="0987654321"),
            Customer(customer_id="009", customer_name="My My", created_date="27.03.2023",phone_number="0994511234"),
            Customer(customer_id="010", customer_name="Hải Yến", created_date="27.03.2023",phone_number="0987654321"),
            Customer(customer_id="011", customer_name="My My", created_date="27.03.2023",phone_number="0994511234"),
            Customer(customer_id="012", customer_name="Hải Yến", created_date="27.03.2023",phone_number="0987654321"),
            Customer(customer_id="013", customer_name="My My", created_date="27.03.2023",phone_number="0994511234"),
            Customer(customer_id="014", customer_name="Hải Yến", created_date="27.03.2023",phone_number="0987654321"),
            Customer(customer_id="015", customer_name="My My", created_date="27.03.2023",phone_number="0994511234"),
            Customer(customer_id="016", customer_name="Hải Yến", created_date="27.03.2023",phone_number="0987654321"),
            Customer(customer_id="017", customer_name="My My", created_date="27.03.2023",phone_number="0994511234"),
            Customer(customer_id="018", customer_name="Hải Yến", created_date="27.03.2023",phone_number="0987654321"),
            Customer(customer_id="019", customer_name="My My", created_date="27.03.2023",phone_number="0994511234"),
            Customer(customer_id="020", customer_name="Hải Yến", created_date="27.03.2023",phone_number="0987654321"),
            Customer(customer_id="021", customer_name="My My", created_date="27.03.2023",phone_number="0994511234"),
            Customer(customer_id="022", customer_name="Hải Yến", created_date="27.03.2023",phone_number="0987654321"),
        ]
        paginator = Paginator(customers, 10)
        page_number = request.GET.get('page')
        if not page_number:
            page_number = 1
        
        page_customers = paginator.get_page(page_number)
        return render(request,'../templates/customers.html', {'customers': page_customers})