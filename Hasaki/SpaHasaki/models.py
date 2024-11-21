from django.db import models

# Create your models here.
class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    customer_name = models.CharField(max_length=255, null=False)
    phone_number = models.CharField(max_length=10, null=True)
    email = models.EmailField(max_length=255, null=True)
    created_date = models.DateTimeField(null=False, auto_now=True)

class Service(models.Model):
    service_id = models.AutoField(primary_key=True)
    service_name = models.CharField(max_length=255, null=False)
    description = models.TextField(max_length=1024, null=True)

class Employee(models.Model):
    employee_id = models.AutoField(primary_key=True)
    employee_name = models.CharField(max_length=255, null=False)
    email = models.EmailField(max_length=255, null=True)
    phone_number = models.CharField(max_length=10, null=False)
    password = models.CharField(max_length=512, null=False)
    created_date = models.DateTimeField(null=False, auto_now=True)

class Appointment(models.Model):
    appointment_id = models.AutoField(primary_key=True)
    customer_id = models.ForeignKey(Customer, to_field='customer_id', on_delete=models.CASCADE)
    service_id = models.ForeignKey(Service, to_field='service_id', on_delete=models.CASCADE)
    employee_id = models.ForeignKey(Employee, to_field='employee_id', on_delete=models.CASCADE)
    appointment_date = models.DateTimeField(null=False, auto_now=True)
    start_time = models.DateTimeField(null=False)
    end_time = models.DateTimeField(null=False)
    status = models.IntegerField(null=False)
    note = models.TextField(null=True)

class Feedback(models.Model):
    request_id = models.AutoField(primary_key=True)
    customer_id = models.ForeignKey(Customer, to_field='customer_id', on_delete=models.CASCADE)
    employee_id = models.ForeignKey(Employee, to_field='employee_id', on_delete=models.CASCADE)
    service_id = models.ForeignKey(Service, to_field='service_id', on_delete=models.CASCADE)
    status = models.IntegerField(null=False)
    priority = models.IntegerField(null=False)
    request_content = models.TextField(null=False)
    request_date = models.DateTimeField(null=False, auto_now=True)