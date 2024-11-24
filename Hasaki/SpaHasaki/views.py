from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.core.paginator import Paginator
from datetime import datetime as dt, timedelta, date
from .models import Customer, Appointment, Service, Employee, Feedback, WorkShifts
from .helpers import get_appointment, read_data
from .enums import AppointmentStatusType, DeletedType

tables = [
    'Customers', 
    'Services', 
    'Employees', 
    'Appointments', 
    'Feedback', 
    'WorkShifts'
]

def home(request):
    if request.method == "GET":
        for table_name in tables:
            if (table_name == "Customers" and Customer.objects.all().values().count() > 0) or \
                (table_name == "Services" and Service.objects.all().values().count() > 0) or \
                (table_name == "Appointments" and Appointment.objects.all().values().count() > 0) or \
                (table_name == "Employees" and Employee.objects.all().values().count() > 0) or \
                (table_name == "Feedback" and Feedback.objects.all().values().count() > 0) or \
                (table_name == "WorkShifts" and WorkShifts.objects.all().values().count() > 0):
                continue

            lst_data = read_data(table_name)
            for data in lst_data:
                if table_name == "Customers":
                    if not Customer.objects.filter(customer_id=data['customer_id']):
                        customer = Customer(customer_id=data['customer_id'],
                                            customer_name=data['customer_name'],
                                            phone_number=data['phone_number'],
                                            email=data['email'],
                                            created_date=data['created_date'],
                                            is_delete=data['is_delete'])
                        customer.save()
                elif table_name == "Services":
                    if not Service.objects.filter(service_id=data['service_id']):
                        service = Service(service_id=data['service_id'],
                                          service_name=data['service_name'],
                                          description=data['description'])
                        service.save()
                elif table_name == "Employees":
                    if not Employee.objects.filter(employee_id=data['employee_id']):
                        employee = Employee(employee_id=data['employee_id'],
                                            employee_name=data['employee_name'],
                                            email=data['email'],
                                            phone_number=data['phone_number'],
                                            password=data['password'],
                                            created_date=data['created_date'])
                        employee.save()
                elif table_name == "Appointments":
                    if not Appointment.objects.filter(appointment_id=data['appointment_id']):
                        appointment = Appointment(appointment_id=data['appointment_id'],
                                                  customer_id=data['customer_id'],
                                                  service_id=data['service_id'],
                                                  employee_id=data['employee_id'],
                                                  appointment_date=dt.strptime(data['appointment_date'], "%d/%m/%Y").date(),
                                                  start_time=data['start_time'],
                                                  end_time=data['end_time'],
                                                  status=data['status'],
                                                  note=data['note'],
                                                  is_delete=data['is_delete'])
                        appointment.save()
                elif table_name == "Feedback":
                    if not Feedback.objects.filter(request_id=data['request_id']):
                        feedback = Feedback(request_id=data['request_id'],
                                            customer_id=data['customer_id'],
                                            employee_id=data['employee_id'],
                                            service_id=data['service_id'],
                                            status=data['status'],
                                            prioritize=data['prioritize'],
                                            request_content=data['request_content'],
                                            request_date=data['request_date'],
                                            is_delete=data['is_delete'])
                        feedback.save()
                elif table_name == "WorkShifts":
                    if not WorkShifts.objects.filter(shifts_id=data['shifts_id']):
                        workShifts = WorkShifts(shifts_id=data['shifts_id'],
                                                employee_id=data['employee_id'],
                                                shifts_date=data['shifts_date'],
                                                shifts_detail=data['shifts_detail'],
                                                is_delete=data['is_delete'])
                        workShifts.save()
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
    
def schedules(request):
    if request.method == 'GET':
        year = request.GET.get('year')
        month = request.GET.get('month')
        day = request.GET.get('day')

        today = dt.today()

        # Convert to integers (with defaults for current year, month, and day)
        year = int(year) if year else today.year
        month = int(month) if month else today.month
        day = int(day) if day else today.day
        appointments = get_appointment(year=year, month=month, day=day)
        data = dict()

        for key in appointments.keys():
            data[key] = []
            for item in appointments[key]:
                info = {
                    'appointment':item['appointment_info'],
                    'customer':Customer.objects.get(customer_id=item['appointment_info']['customer_id']),
                    'employee':Employee.objects.get(employee_id=item['appointment_info']['employee_id']),
                    'service':Service.objects.get(service_id=item['appointment_info']['service_id'])
                }
                data[key].append(info)

        context = {
            'data': data,
            'filterDate': date(year,month,day).strftime('%Y-%m-%d')
        }
        return render(request,'../templates/appointments.html', {"context": context})
    
def customers(request):
    if request.method == 'GET':
        customers = Customer.objects.filter(is_delete=DeletedType.AVAILABLE.value).values()
        paginator = Paginator(customers, 12)
        page_number = request.GET.get('page')
        if not page_number:
            page_number = 1
        
        customers_per_page = paginator.get_page(page_number)
        return render(request,'../templates/customers.html', {'customers': customers_per_page})

def cancel_appointment(request, id):
    if request.method == 'POST':
        previous_url = request.META.get('HTTP_REFERER')
        appointment = Appointment.objects.get(appointment_id=id)

        if appointment:
            appointment.status = AppointmentStatusType.CANCEL.value
            appointment.save()
            return redirect(previous_url)
        
def detail_customer(request, id):
    if request.method == 'GET':
        year = request.GET.get('year')
        month = request.GET.get('month')
        day = request.GET.get('day')

        today = dt.today()
        year = int(year) if year else today.year
        month = int(month) if month else today.month
        day = int(day) if day else today.day

        customer = Customer.objects.get(customer_id=id)
        appointments = Appointment.objects.filter(customer_id=id)\
            .filter(appointment_date=date(year=year, month=month, day=day)).values()

        context = {
            'customer': customer,
            'appointments': appointments,
            'filterDate': date(year=year, month=month, day=day).strftime('%Y-%m-%d')
        }
        return render(request, '../templates/customer_detail_info.html', {'context':context})
    
def delete_customer(request, id):
    if request.method == 'POST':
        customer = Customer.objects.get(customer_id=id)
        if customer:
            customer.is_delete = DeletedType.DELETED.value
            customer.save()
            return redirect('/customers')

@csrf_protect
def edit_customer(request, id):
    if request.method == 'POST':
        customer = Customer.objects.get(customer_id=id)
        if customer:
            customer.customer_name = request.POST.get('customer_name')
            customer.email = request.POST.get('email')
            customer.phone_number = request.POST.get('phone_number')
            customer.save()
            return redirect('/customers/detail/{0}'.format(id))
        
