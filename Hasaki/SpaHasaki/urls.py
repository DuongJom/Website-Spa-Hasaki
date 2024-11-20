from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('login-options', views.login_options, name='login-options'),
    path('forgot-password/phone-verify', views.phone_verify, name='phone-verify'),
    path('reset-password', views.reset_password, name='reset-password'),
    path('schedules', views.schedule, name='schedule'),
    path('customers', views.customers, name='customers')
]