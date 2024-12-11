import calendar
import json
import random
from django.contrib import messages
from django.contrib.auth import login as auth_login, authenticate
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Q
from django.core.paginator import Paginator
from datetime import datetime as dt, timedelta, date
from .models import Customer, Appointment, Service, Employee, Feedback, WorkShifts, Messenger, Account, FeedbackDetail
from .helpers import get_appointment, read_data
from .enums import AppointmentStatusType, DeletedType, RoleType

User = get_user_model()

tables = {
    'ACCOUNT': 'Accounts',
    'CUSTOMER': 'Customers', 
    'SERVICE': 'Services', 
    'EMPLOYEE': 'Employees', 
    'APPOINTMENT': 'Appointments', 
    'FEEDBACK': 'Feedback', 
    'WORK_SHIFT': 'WorkShifts',
    'MESSENGER': 'Messengers'
}

def home(request):
    if request.method == "GET":
        customer_id = request.session.get('customer')
        customer = Customer.objects.get(customer_id=int(customer_id))
            
        context = {
            'customer': customer
        }
        return render(request,'../templates/home.html', {'context': context})
    
@csrf_protect
def login(request):
    if request.method == 'GET':
        for key, value in tables.items():
            if (value == tables['ACCOUNT'] and Account.objects.all().values().count() > 0) or \
                (value == tables['CUSTOMER'] and Customer.objects.all().values().count() > 0) or \
                (value == tables['SERVICE'] and Service.objects.all().values().count() > 0) or \
                (value == tables['APPOINTMENT'] and Appointment.objects.all().values().count() > 0) or \
                (value == tables['EMPLOYEE'] and Employee.objects.all().values().count() > 0) or \
                (value == tables['FEEDBACK'] and Feedback.objects.all().values().count() > 0) or \
                (value == tables['WORK_SHIFT'] and WorkShifts.objects.all().values().count() > 0) or \
                (value == tables['MESSENGER'] and Messenger.objects.all().values().count() > 0):
                continue

            lst_data = read_data(value)
            for data in lst_data:
                if value == tables['ACCOUNT']:
                    if not Account.objects.filter(username=data['username']):
                        account = Account(account_id=data['account_id'],
                                          username=data['username'],
                                          password=data['password'],
                                          role=data['role'],
                                          is_delete=data['is_delete'])
                        account.save()

                    if not User.objects.filter(username=data['username']).exists():
                        User.objects.create_superuser(username=data['username'], email=data['username'], password=data['password'])
                        
                if value == tables['CUSTOMER']:
                    if not Customer.objects.filter(customer_id=data['customer_id']):
                        customer = Customer(customer_id=data['customer_id'],
                                            customer_name=data['customer_name'],
                                            phone_number=data['phone_number'],
                                            email=data['email'],
                                            created_date=data['created_date'],
                                            is_delete=data['is_delete'])
                        customer.save()
                elif value == tables['SERVICE']:
                    if not Service.objects.filter(service_id=data['service_id']):
                        service = Service(service_id=data['service_id'],
                                          service_name=data['service_name'],
                                          description=data['description'])
                        service.save()
                elif value == tables['EMPLOYEE']:
                    if not Employee.objects.filter(employee_id=data['employee_id']):
                        employee = Employee(employee_id=data['employee_id'],
                                            employee_name=data['employee_name'],
                                            email=data['email'],
                                            phone_number=data['phone_number'],
                                            created_date=data['created_date'])
                        employee.save()
                elif value == tables['APPOINTMENT']:
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
                elif value == tables['FEEDBACK']:
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
                elif value == tables['WORK_SHIFT']:
                    if not WorkShifts.objects.filter(shifts_id=data['shifts_id']):
                        workShifts = WorkShifts(shifts_id=data['shifts_id'],
                                                employee_id=data['employee_id'],
                                                shifts_date=data['shifts_date'],
                                                shifts_detail=data['shifts_detail'],
                                                is_delete=data['is_delete'])
                        workShifts.save()
                elif value == tables['MESSENGER']:
                    if not Messenger.objects.filter(messenger_id=data['messenger_id']):
                        messenger = Messenger(messenger_id=data['messenger_id'],
                                              customer_id=data['customer_id'],
                                              employee_id=data['employee_id'],
                                              message_id=data['message_id'],
                                              message=data['message'],
                                              is_sent_from_customer=data['is_sent_from_customer'],
                                              sent_time=data['sent_time'],
                                              is_resolved=data['is_resolved'],
                                              is_delete=data['is_delete'])
                        messenger.save()
        return render(request, '../templates/login.html')
    
    username = request.POST.get('username')
    password = request.POST.get('password')

    if not username or not password:
        messages.error(request, 'Vui lòng kiểm tra lại tài khoản đăng nhập!')
        return redirect(request.path)
    
    user = authenticate(request, username=username, password=password)
    auth_login(request=request, user=user)

    account = Account.objects.filter(username=username, password=password).first()
    if account:
        messages.success(request, "Đăng nhập thành công!")
        if account.role == RoleType.CUSTOMER.value:
            customer = Customer.objects.filter(email=account.username).first()
            if customer:
                request.session['customer'] = customer.customer_id
            return redirect("/home")
        else:
            employee = Employee.objects.filter(email=account.username).first()
            if employee:
                request.session['employee'] = employee.employee_id
            return redirect("/schedules")
            
        
    messages.error(request, 'Tài khoản không tồn tại!')
    return redirect(request.path)

@csrf_protect
def signup(request):
    if request.method == 'GET':
        return render(request, '../templates/signup.html')
    
    full_name = request.POST.get('fullname')
    email = request.POST.get('email')
    phone = request.POST.get('phone')
    password = request.POST.get('password')
    confirm_password = request.POST.get('confirm_password')

    if password != confirm_password:
        messages.error(request, 'Xác nhận mật khẩu không chính xác!')
        return redirect(request.path)

    if len(phone) < 9 or len(phone) > 11:
        messages.error(request, 'Số điện thoại không hợp lệ!')
        return redirect(request.path)
    
    try:
        customer = Customer(
            customer_name=full_name,
            email=email,
            phone_number=phone
        )
        customer.save()
        account = Account(
            username=email,
            password=password,
            role=0
        )
        account.save()

        User.objects.create_superuser(username=email, email=email, password=password)
        messages.success(request, 'Đăng ký tài khoản thành công!')
    except Exception as e:
        messages.error(request, 'Đăng ký tìa khoản thất bại!')
        return redirect(request.path)
    return redirect('/login')
@csrf_protect
def appointment_booking(request):
    customer_id = request.session.get('customer')
    if not customer_id:
        return redirect('/login')
    
    services = Service.objects.all()
    customer = Customer.objects.filter(customer_id=customer_id).first()

    if request.method == "GET":
        context = {
            'isSuccess': False,
            'services': services,
            'customer': customer
        }
        return render(request,'../templates/appointment_booking.html', {'context': context})
    
    # Check validity of fields on form
    note = request.POST.get('note')
    service = request.POST.get('service')
    appointment_date = request.POST.get('appointment_date')
    start_time = request.POST.get('start_time')
    service_time = request.POST.get('service_time')
    end_time = None

    if (int(service) == -1) or \
        (appointment_date == '') or (start_time == ''):
        messages.error(request,'Vui lòng điền đủ thông tin!')
        context = {
            'isSuccess': False,
            'services': services,
            'customer': customer
        }
        return render(request, '../templates/appointment_booking.html', {'context': context})
    
    booking_time = dt.strptime(start_time, '%H:%M').time()
    range_time = None
    if booking_time.hour >= 9 and booking_time.hour < 13:
        range_time = "Sáng (9h - 13h00)"
    elif booking_time.hour >= 13 and booking_time.hour < 17:
        range_time = "Chiều (13h00 - 17h00)"
    else:
        range_time = "Tối (17h00 - 20h00)"

    available_employees = WorkShifts.objects.filter(shifts_date=appointment_date).filter(shifts_detail__contains=range_time).values()
    if available_employees.count() == 0:
        messages.error(request, "Hiện tại không có nhân viên cho khung giờ này! Vui lòng chọn khung giờ khác!")
        return redirect(request.path)
    
    if available_employees.count() == 5:
        messages.error(request, "Hiện tại đã full nhân viên cho khung giờ này! Vui lòng chọn khung giờ khác!")
        return redirect(request.path)

    service_obj = Service.objects.filter(service_id=service).first()
    minutes = (float(service_time) * 60) if service_time else 30
    end_time = (dt.strptime(str(start_time), "%H:%M") + timedelta(minutes=minutes)).time()
    employee_id = available_employees.first()['employee_id']
    employee = Employee.objects.get(employee_id=employee_id)

    appointment = Appointment(
        customer = customer,
        service = service_obj,
        employee = employee,
        appointment_date = appointment_date,
        start_time = dt.strptime(str(start_time), "%H:%M").time(),
        end_time = end_time,
        status = AppointmentStatusType.INCOMPLETE.value,
        note = note
    )
    appointment.save()

    context = {
        'isSuccess': True,
        'customer_name': customer.customer_name,
        'phone': customer.phone_number,
        'email': customer.email,
        'service': service_obj.service_name if service_obj else "Không dịch vụ",
        'appointment_date': appointment_date,
        'note': note,
        'start_time': start_time,
        'end_time': f"{str(end_time.hour).zfill(2)}:{str(end_time.minute).zfill(2)}",
        'start_clock_type': "AM" if int(str(start_time).split(":")[0]) < 12 else "PM",
        'end_clock_type': "AM" if end_time.hour < 12 else "PM"
    }
    return render(request, '../templates/appointment_booking.html', {'context': context})

@csrf_protect
def support(request):
    services = Service.objects.all().values()
    customer_id = request.session.get('customer')
    if not customer_id:
        return redirect('/login')
    
    customer = Customer.objects.filter(customer_id=int(customer_id)).first()

    if request.method == 'GET':
        context = {
            'isShowModal': False,
            'services': services,
            'customer': customer
        }
        return render(request, '../templates/request.html', {'context': context})
    
    service = request.POST.get('service')
    content = request.POST.get('request_content')
    try:
        feedback = Feedback(
            customer=customer,
            service=Service.objects.get(service_id=int(service)),
            request_content=content,
            request_date=dt.strptime(dt.today().strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")
        )
        feedback.save()

        context = {
            'customer': customer,
            'customer_name': customer.customer_name,
            'phone': customer.phone_number,
            'service': Service.objects.get(service_id=service),
            'content': content,
            'request_date': feedback.request_date,
            'isShowModal': True,
            'services': services
        }
    except Exception as e:
        context = {
            'customer': customer,
            'customer_name': customer.customer_name,
            'phone': customer.phone_number,
            'service': Service.objects.get(service_id=service),
            'content': content,
            'isShowModal': False,
            'services': services
        }
        print(e)
    return render(request,'../templates/request.html', {'context': context})

@csrf_protect
def register_work_shifts(request):
    employee_id = request.session.get('employee')
    employee = Employee.objects.get(employee_id=employee_id)

    if request.method == 'GET':
        if not employee_id:
            return redirect('/login')
        context = {
            'isSuccess': False,
            'employee': employee,
            'default_date': dt.today().strftime('%Y-%m-%d')
        }
        return render(request, '../templates/register_work_shifts.html', {'context': context})
    
    shifts_date = request.POST.get('shifts_date')
    shifts_detail = request.POST.get('shifts_detail')

    if dt.strptime(shifts_date, '%Y-%m-%d').date() < dt.today().date():
        messages.error(request, 'Ngày đăng ký không hợp lệ!')
        context = {
            'isSuccess': False,
            'employee': employee,
            'default_date': dt.strptime(shifts_date, '%Y-%m-%d').strftime('%Y-%m-%d')
        }
        return render(request, '../templates/register_work_shifts.html', {'context': context})

    if int(shifts_detail) < 0:
        messages.error(request, 'Vui lòng chọn ca làm việc!')
        return redirect(request.META.get('HTTP_REFERER'))
    
    detail = None
    if int(shifts_detail) == 0:
        detail = "Sáng (9h - 13h00)"
    elif int(shifts_detail) == 1:
        detail = "Chiều (13h00 - 17h00)"
    else:
        detail = "Tối (17h00 - 20h00)"

    work_shift = WorkShifts.objects.filter(
        employee_id=employee_id, 
        shifts_date=dt.strptime(shifts_date,'%Y-%m-%d').date()
    ).values().first()

    if work_shift:
        details = [detail for detail in work_shift['shifts_detail'].split(';')]
        if detail in details:
            messages.error(request, 'Vui lòng chọn ca làm khác!')
            return redirect(request.path)
        
        WorkShifts.objects.filter(
            employee_id=employee_id, 
            shifts_date=dt.strptime(shifts_date,'%Y-%m-%d').date()
        ).update(shifts_detail = work_shift['shifts_detail'] + ';' + detail)
    else:
        work_shift = WorkShifts(
            employee = employee,
            shifts_date = dt.strptime(shifts_date, '%Y-%m-%d').date(),
            shifts_detail = detail
        )
        work_shift.save()

    context = {
        'isSuccess': True,
        'employee': employee,
        'default_date': dt.today().strftime('%Y-%m-%d'),
        'info':{
            'employee_name': employee.employee_name,
            'phone_number': employee.phone_number,
            'shifts_date': dt.strptime(shifts_date, '%Y-%m-%d').date(),
            'shifts_detail': detail
        }
    }
    return render(request, '../templates/register_work_shifts.html', {'context': context})

def work_shifts(request):
    if request.method == 'GET':
        if not request.session.get('employee'):
            return redirect('/login')
        
        month = int(request.GET.get('month')) if request.GET.get('month') else dt.today().month
        year = int(request.GET.get('year')) if request.GET.get('year') else dt.today().year
        week = int(request.GET.get('week')) if request.GET.get('week') else 1
        employee_id = request.session.get('employee')

        if not employee_id:
            messages.error(request, 'Vui lòng đăng nhập để xem thông tin!')
            return redirect(request.path)
        
        if not month or not year:
            month = dt.today().month
            year = dt.today().year

        cal = calendar.monthcalendar(year, month)
        week_days = cal[week - 1]
        dates_of_week = []
        for i, day in enumerate(week_days):
            if day != 0:
                dates_of_week.append(date(year, month, day))

        morning = "Sáng (9h - 13h00)"
        afternoon = "Chiều (13h00 - 17h00)"
        evening = "Tối (17h00 - 20h00)" 
        data = []
        for day in dates_of_week:
            work_shift = WorkShifts.objects.filter(
                employee_id=employee_id, 
                shifts_date=day
            ).first()
            info = dict()
            if work_shift:
                details = [detail for detail in work_shift.shifts_detail.split(';')]
                info = {
                    'day': day,
                    'is_morning': True if morning in details else False,
                    'is_afternoon': True if afternoon in details else False,
                    'is_evening': True if evening in details else False
                }
            else:
                info = {
                    'day': day,
                    'is_morning':  False,
                    'is_afternoon': False,
                    'is_evening': False
                }
            data.append(info)

        context = {
            'current_date': dt.today().strftime('%Y-%m'),
            'week_days': dates_of_week,
            'week_number': week,
            'weeks': [i for i in range(1, len(cal) + 1)],
            'data': data,
            'employee': Employee.objects.get(employee_id=employee_id)
        }
        return render(request, '../templates/personal_work_shifts.html', {'context': context})

# Function to generate a random OTP
def generate_otp():
    return str(random.randint(100000, 999999))

# View to send the OTP via SMS
@csrf_protect
def email_verify(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        is_email_exist = Account.objects.filter(username=email).exists() and User.objects.filter(username=email).exists()

        if not email or not is_email_exist:
            messages.error(request, 'Please provide a valid email address.')
            return redirect(request.path)

        request.session['email'] = email

        # Generate OTP
        otp_code = generate_otp()

        # Store OTP in session (for verification later)
        request.session['otp'] = otp_code

        try:
            # Send OTP via email
            send_mail(
                'Your OTP Code',  # Subject
                f'Your OTP code is {otp_code}. Please use it to verify your email.',  # Message content
                settings.DEFAULT_FROM_EMAIL,  # From email (use the email from settings)
                [email],  # Recipient email
                fail_silently=False,  # Set to True to suppress errors
            )
            messages.success(request, 'OTP sent successfully to your email!')
            return redirect('/forgot-password/otp-verify')  # Redirect to OTP verification page
        except Exception as e:
            messages.error(request, f"Error sending OTP")
            print(str(e))
            return redirect(request.path)
        
    return render(request, '../templates/email_verification.html')

@csrf_protect
def otp_verify(request):
    if request.method == 'GET':
        return render(request, '../templates/otp_verification.html')
    
    code1 = request.POST.get('code1')
    code2 = request.POST.get('code2')
    code3 = request.POST.get('code3')
    code4 = request.POST.get('code4')
    code5 = request.POST.get('code5')
    code6 = request.POST.get('code6')
    otp = code1 + code2 + code3 + code4 + code5 + code6

    if otp == request.session.get('otp'):
        messages.success(request, 'Xác thực OTP thành công!')
        return redirect('/reset-password')
    
    messages.error(request, 'OTP không hợp lệ!')
    return redirect('/forgot-password/email-verify')

def logout(request):
    request.session.pop('employee', None)
    request.session.pop('customer', None)
    return redirect('/')

@csrf_protect
def reset_password(request):
    if request.method == 'GET':
        return render(request, '../templates/new_password.html')
    
    new_password = request.POST.get('new_password')
    confirm_password = request.POST.get('confirm_password')

    if not new_password or not confirm_password:
        messages.error(request, 'Vui lòng điền thông tin password!')
        return redirect(request.path)
    
    if new_password != confirm_password:
        messages.error(request, 'Xác nhận mật khẩu không hợp lệ!')
        return redirect(request.path)
    
    email = request.session.get('email')
    account = Account.objects.filter(username=email).first()
    if account:
        account.password = new_password
        account.save()

    user = User.objects.filter(email=email).first()
    if user:
        user.delete()
        User.objects.create_superuser(username=email, email=email, password=new_password)
    messages.success(request, 'Cập nhật mật khẩu thành công!')
    return redirect('/')

@csrf_protect
def schedules(request):
    if not request.session.get('employee'):
        return redirect('/login')
    
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

        employee_id = request.session.get('employee')
        employee = Employee.objects.get(employee_id=int(employee_id))
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
            'filterDate': date(year,month,day).strftime('%Y-%m-%d'),
            'employee': employee
        }
        return render(request,'../templates/appointments.html', {"context": context})
    
    data = json.loads(request.body)
    status = data.get('status')
    appointment_id = data.get('appointment_id')
    appointment = Appointment.objects.filter(appointment_id=appointment_id).first()
    if appointment:
        appointment.status = int(status)
        appointment.save()
        messages.success(request, 'Cập nhật trạng thái thành công!')
    else:
        messages.error(request, 'Lịch hẹn không tồn tại')
    return redirect(request.path)

def customers(request):
    # Redirect to login if the employee is not in session
    if not request.session.get('employee'):
        return redirect('/login')
    
    # Handle GET request
    if request.method == 'GET':
        # Get the search parameter from query parameters
        search = request.GET.get('search', '')
        sort = request.GET.get('sort', 0)

        # Filter customers based on whether they are deleted or not
        customers = Customer.objects.filter(is_delete=DeletedType.AVAILABLE.value).order_by('customer_id')

        # If search parameter exists, filter based on it
        if search:
            customers = customers.filter(
                Q(customer_name__icontains=search) |
                Q(email__icontains=search) |
                Q(phone_number__icontains=search[1:])
            )

        if int(sort) == 0:
            customers = customers.order_by('-created_date')
        elif int(sort) == 1:
            customers = customers.order_by('customer_name')

        # Set up pagination (12 items per page)
        paginator = Paginator(customers, 12)
        page_number = request.GET.get('page', 1)
        
        # Fetch employee data from the session
        employee_id = request.session.get('employee')
        employee = None
        if employee_id:
            employee = Employee.objects.get(employee_id=int(employee_id))

        # Get the paginated customers
        customers_per_page = paginator.get_page(page_number)
        
        # Pass data to the template
        context = {
            'customers': customers_per_page,
            'employee': employee,
            'search': search,  # Include the search term in the context
            'sort': int(sort)
        }
        return render(request, 'customers.html', context)

def cancel_appointment(request, appointment_id):
    if request.method == 'POST':
        previous_url = request.META.get('HTTP_REFERER')
        appointment = Appointment.objects.get(appointment_id=appointment_id)

        if appointment:
            appointment.status = AppointmentStatusType.CANCEL.value
            appointment.save()
            return redirect(previous_url)

def detail_customer(request, customer_id):
    if request.method == 'GET':
        if not request.session.get('employee'):
            return redirect('/login')
        
        year = request.GET.get('year')
        month = request.GET.get('month')
        day = request.GET.get('day')

        today = dt.today()
        year = int(year) if year else today.year
        month = int(month) if month else today.month
        day = int(day) if day else today.day

        customer = Customer.objects.get(customer_id=customer_id)
        appointments = Appointment.objects.filter(customer_id=customer_id)\
            .filter(appointment_date=date(year=year, month=month, day=day)).values()

        employee_id = request.session.get('employee')
        employee = None
        if employee_id:
            employee = Employee.objects.get(employee_id=int(employee_id))

        context = {
            'customer': customer,
            'appointments': appointments,
            'filterDate': date(year=year, month=month, day=day).strftime('%Y-%m-%d'),
            'employee': employee
        }
        return render(request, '../templates/customer_detail_info.html', {'context':context})
    
def delete_customer(request, customer_id):
    if request.method == 'POST':
        customer = Customer.objects.get(customer_id=customer_id)
        if customer:
            appointments = Appointment.objects.filter(customer_id=customer.customer_id)
            if appointments:
                appointments.update(is_delete=DeletedType.DELETED.value)

            customer.is_delete = DeletedType.DELETED.value
            customer.save()
            return redirect("/customers")

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

def messenger(request):
    if request.method == 'GET':
        if not request.user.is_authenticated:
            return redirect('/login')
        
        username = request.GET.get('username')
        if username:
            customer = Customer.objects.filter(email=username).first()

        customers = Messenger.objects.values('customer_id').distinct()
        data = []
        if customers.count() > 0:
            for customer in customers:
                messages = Messenger.objects.filter(customer_id=customer['customer_id']).values('message').order_by('-sent_time')
                info = {
                    'customer': Customer.objects.get(customer_id=customer['customer_id']),
                    'messages': messages
                }
                data.append(info)
        context = {
            'data': data
        }

        return render(request, '../templates/messenger.html', {'context': context})

def customer_chat(request):
    customer_id = request.session.get('customer')
    if not customer_id:
        return redirect('/login')
        
    if request.method == 'GET':
        context = {
            'customer': Customer.objects.filter(customer_id=customer_id).first()
        }
        return render(request, '../templates/customer_chat.html', {'context': context})
    
def feedbacks(request):
    employee_id = request.session.get('employee')
    if request.method == 'GET':
        if not employee_id:
            return redirect('/login')
        
        search = request.GET.get('search')
        status = request.GET.get('status')
        prioritize = request.GET.get('prioritize')
        date_filter = request.GET.get('date_filter')

        employee = Employee.objects.get(employee_id=employee_id)
        feedbacks = Feedback.objects.all()

        if search and len(search.strip()) != 0:
            feedbacks = feedbacks.filter(request_content__icontains=search)

        if status and int(status) != -1:
            feedbacks = feedbacks.filter(status=int(status))

        if prioritize and int(prioritize) != -1:
            feedbacks = feedbacks.filter(prioritize=int(prioritize))
        
        if date_filter:
            feedbacks = feedbacks.filter(request_date=dt.strptime(date_filter,'%Y-%m-%d %H:%M:%S'))

        info = []

        for feedback in feedbacks.values():
            customer = Customer.objects.filter(customer_id=feedback['customer_id']).values().first()
            service = Service.objects.filter(service_id=feedback['service_id']).values().first()
            data = {
                'feedback': feedback,
                'customer': customer,
                'service': service,
            }
            info.append(data)
            
        context = {
            'employee': employee,
            'info': info,
            'search': search if search else "",
            'status': int(status) if status else 0,
            'priority': int(prioritize) if prioritize else 0,
            'date_filter': date_filter if date_filter else dt.today(),     
        }
        return render(request, '../templates/feedback.html', {'context': context})

@csrf_protect
def feedback_detail(request, feedback_id):
    employee_id = request.session.get('employee')
    if not employee_id:
            return redirect('/login')
    
    feedback = Feedback.objects.get(request_id=feedback_id)
    employee = Employee.objects.get(employee_id=employee_id)
    customer = Customer.objects.get(customer_id=feedback.customer_id)
    service = Service.objects.get(service_id=feedback.service_id)
    feedback_detail = FeedbackDetail.objects.filter(feedback_id=feedback.request_id).values()

    if request.method == 'GET':
        context = {
            'feedback': feedback,
            'customer': customer,
            'employee': employee,
            'service': service,
            'detail': feedback_detail
        }
        return render(request, '../templates/feedback_detail.html', {'context': context})
    
    data = json.loads(request.body)
    reply_content = data.get('reply_content')
    reply_time = data.get('reply_time')
    status = data.get('status')
    prioritize = data.get('prioritize')

    if reply_content and reply_time:
        detail = FeedbackDetail(
            feedback_id=feedback.request_id,
            reply_content=reply_content,
            reply_time=dt.strptime(reply_time, "%Y-%m-%d %H:%M")
        )
        detail.save()

    if feedback:
        if status and int(status) != -1:
            feedback.status = int(status)
        if prioritize and int(prioritize) != -1:
            feedback.prioritize = int(prioritize)
        feedback.save()
        messages.success(request, 'Cập nhật phản hồi thành công!')
    else:
        messages.error(request, 'Cập nhật phản hồi thất bại! Vui lòng kiểm tra lại thông tin!')
        return redirect(request.path)

    feedback = Feedback.objects.get(request_id=feedback_id)
    employee = Employee.objects.get(employee_id=employee_id)
    customer = Customer.objects.get(customer_id=feedback.customer_id)
    service = Service.objects.get(service_id=feedback.service_id)
    feedback_detail = FeedbackDetail.objects.filter(feedback_id=feedback.request_id).values()

    context = {
            'feedback': feedback,
            'customer': customer,
            'employee': employee,
            'service': service,
            'detail': feedback_detail
    }
    return render(request, '../templates/feedback_detail.html', {'context': context})

def customer_feedback(request):
    customer_id = request.session.get('customer')
    if not customer_id:
        return redirect('/login')

    if request.method == 'POST':
        pass
    
    customer = Customer.objects.filter(customer_id=customer_id).first()
    feedbacks = Feedback.objects.filter(customer_id=customer_id)
    data = []
    
    for feedback in feedbacks:
        info = {
            'customer': customer,
            'feedback': feedback,
            'service': Service.objects.filter(service_id=feedback.service_id).first()
        }
        data.append(info)

    context = {
        'customer': customer,
        'feedbacks': data
    }
    return render(request, '../templates/customer_feedback.html',{'context': context})

def customer_feedback_detail(request, feedback_id):
    customer_id = request.session.get('customer')
    if not customer_id:
        return redirect('/login')
    
    customer = Customer.objects.filter(customer_id=customer_id).first()
    feedbacks = Feedback.objects.filter(customer_id=customer_id)
    feedback = Feedback.objects.filter(request_id=feedback_id).first()
    service = Service.objects.filter(service_id=feedback.service_id).first()
    feedback_detail = FeedbackDetail.objects.filter(feedback_id=feedback_id)
    data = []
    
    for fb in feedbacks:
        info = {
            'customer': customer,
            'feedback': fb,
            'service': Service.objects.filter(service_id=fb.service_id).first()
        }
        data.append(info)

    if request.method == 'GET':
        context = {
            'customer': customer,
            'feedbacks': data,
            'feedback': feedback,
            'service': service,
            'detail': feedback_detail
        }
        return render(request, '../templates/customer_feedback_detail.html', {'context': context})
    
    data = json.loads(request.body)
    reply_content = data.get('reply_content')
    reply_time = data.get('reply_time')

    if reply_content and reply_time:
        detail = FeedbackDetail(
            feedback_id=feedback.request_id,
            reply_content=reply_content,
            reply_time=dt.strptime(reply_time, "%Y-%m-%d %H:%M"),
            reply_to_customer = 0
        )
        detail.save()
    
    return redirect(request.path)