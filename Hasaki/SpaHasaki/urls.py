from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login', views.login, name='login'),
    path('home', views.home, name='home'),
    path('booking', views.appointment_booking, name='booking'),
    path('forgot-password/phone-verify', views.phone_verify, name='phone-verify'),
    path('reset-password', views.reset_password, name='reset-password'),
    path('schedules', views.schedules, name='schedule'),
    path('schedules/detail/<int:id>', views.detail_appointment, name='detail-appointment'),
    path('customers', views.customers, name='customers'),
]