from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login, name='login'),
    path('home', views.home, name='home'),
    path('booking', views.appointment_booking, name='booking'),
    path('login-options', views.login_options, name='login-options'),
    path('forgot-password/phone-verify', views.phone_verify, name='phone-verify'),
    path('reset-password', views.reset_password, name='reset-password'),
    path('schedules', views.schedule, name='schedule'),
    path('customers', views.customers, name='customers')
]