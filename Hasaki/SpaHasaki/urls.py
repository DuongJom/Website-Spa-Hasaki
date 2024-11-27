from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('home', views.home, name='home'),
    path('booking', views.appointment_booking, name='booking'),
    path('forgot-password/phone-verify', views.phone_verify, name='phone-verify'),
    path('reset-password', views.reset_password, name='reset-password'),
    path('schedules', views.schedules, name='schedules'),
    path('cancel-appointment/<int:id>', views.cancel_appointment, name='cancel-appointment'),
    path('customers', views.customers, name='customers'),
    path('customers/detail/<int:id>', views.detail_customer, name='detail-customer'),
    path('customers/delete/<int:id>', views.delete_customer, name='delete-customer'),
    path('customers/edit/<int:id>', views.edit_customer, name='edit-customer'),
    path('messenger', views.messenger, name='messenger'),
    path('messenger/<int:id>', views.chat_content, name='chat'),
    path('support', views.support, name='support'),
    path('register-work-shifts', views.register_work_shifts, name='register-work_shifts'),
]