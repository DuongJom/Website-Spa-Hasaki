from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.core.paginator import Paginator
from datetime import datetime as dt, timedelta
import datetime
from SpaHasaki.models import Customer, Appointment
 
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
        datas = dict()
        for t in times:
            key = datetime.time(hour=t).strftime("%H:%M")
            datas[key] = []
            for appointment in appointments:
                if appointment['appointment'].start_time.hour == t:
                    datas[key].append(appointment)
        return render(request,'appointments.html', {"datas": datas})
    
def customers(request):
    if request.method == 'GET':
        customers = [
            Customer(id="001", name="My My", date_of_birth="11.05.2002", date_create="27.03.2023",phone_number="0994511234"),
            Customer(id="002", name="Hải Yến", date_of_birth="01.01.2002", date_create="27.03.2023",phone_number="0987654321"),
            Customer(id="003", name="My My", date_of_birth="11.05.2002", date_create="27.03.2023",phone_number="0994511234"),
            Customer(id="004", name="Hải Yến", date_of_birth="01.01.2002", date_create="27.03.2023",phone_number="0987654321"),
            Customer(id="005", name="My My", date_of_birth="11.05.2002", date_create="27.03.2023",phone_number="0994511234"),
            Customer(id="006", name="Hải Yến", date_of_birth="01.01.2002", date_create="27.03.2023",phone_number="0987654321"),
            Customer(id="007", name="My My", date_of_birth="11.05.2002", date_create="27.03.2023",phone_number="0994511234"),
            Customer(id="008", name="Hải Yến", date_of_birth="01.01.2002", date_create="27.03.2023",phone_number="0987654321"),
            Customer(id="009", name="My My", date_of_birth="11.05.2002", date_create="27.03.2023",phone_number="0994511234"),
            Customer(id="010", name="Hải Yến", date_of_birth="01.01.2002", date_create="27.03.2023",phone_number="0987654321"),
            Customer(id="011", name="My My", date_of_birth="11.05.2002", date_create="27.03.2023",phone_number="0994511234"),
            Customer(id="012", name="Hải Yến", date_of_birth="01.01.2002", date_create="27.03.2023",phone_number="0987654321"),
            Customer(id="013", name="My My", date_of_birth="11.05.2002", date_create="27.03.2023",phone_number="0994511234"),
            Customer(id="014", name="Hải Yến", date_of_birth="01.01.2002", date_create="27.03.2023",phone_number="0987654321"),
            Customer(id="015", name="My My", date_of_birth="11.05.2002", date_create="27.03.2023",phone_number="0994511234"),
            Customer(id="016", name="Hải Yến", date_of_birth="01.01.2002", date_create="27.03.2023",phone_number="0987654321"),
            Customer(id="017", name="My My", date_of_birth="11.05.2002", date_create="27.03.2023",phone_number="0994511234"),
            Customer(id="018", name="Hải Yến", date_of_birth="01.01.2002", date_create="27.03.2023",phone_number="0987654321"),
            Customer(id="019", name="My My", date_of_birth="11.05.2002", date_create="27.03.2023",phone_number="0994511234"),
            Customer(id="020", name="Hải Yến", date_of_birth="01.01.2002", date_create="27.03.2023",phone_number="0987654321"),
            Customer(id="021", name="My My", date_of_birth="11.05.2002", date_create="27.03.2023",phone_number="0994511234"),
            Customer(id="022", name="Hải Yến", date_of_birth="01.01.2002", date_create="27.03.2023",phone_number="0987654321"),
        ]
        paginator = Paginator(customers, 12)
        page_number = request.GET.get('page')
        if not page_number:
            page_number = 1
        
        page_customers = paginator.get_page(page_number)
        return render(request,'customers.html', {'customers': page_customers})