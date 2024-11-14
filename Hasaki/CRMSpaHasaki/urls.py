"""
URL configuration for CRMSpaHasaki project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import login_options, phone_verify, login, reset_password, get_list_appointments

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login, name='login'),
    path('login-options', login_options, name='login-options'),
    path('forgot-password/phone-verify', phone_verify, name='phone-verify'),
    path('reset-password', reset_password, name='reset-password'),
    path('employee/appointments', get_list_appointments, name='employee-appointments'),
]
