from django.db import models

# Create your models here.
class Customer(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=False)
    gender = models.IntegerField(null=False, default=0) # 0:Male, 1:Female
    date_of_birth = models.DateTimeField(auto_now_add=True)
    phone_number = models.CharField(max_length=10, null=True)
    email = models.EmailField(max_length=255, null=True)
    address = models.CharField(max_length=1024, null=True)
    date_create = models.DateTimeField(null=False, auto_now=True)

class Service(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=False)
    description = models.TextField(max_length=1024, null=True)
    date_create = models.DateTimeField(null=False, auto_now=True)

class Employee(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=False)
    email = models.EmailField(max_length=255, null=True)
    phone_number = models.CharField(max_length=10, null=False)
    password = models.CharField(max_length=512, null=False)
    date_create = models.DateTimeField(null=False, auto_now=True)

class Appointment(models.Model):
    id = models.AutoField(primary_key=True)
    customer_id = models.ForeignKey(Customer, to_field='id', on_delete=models.CASCADE)
    service_id = models.ForeignKey(Service, to_field='id', on_delete=models.CASCADE)
    employee_id = models.ForeignKey(Employee, to_field='id', on_delete=models.CASCADE)
    appointment_date = models.DateTimeField(null=False, auto_now=True)
    start_time = models.DateTimeField(null=False)
    end_time = models.DateTimeField(null=False)
    status = models.IntegerField(null=False)
    note = models.TextField(null=True)
    date_create = models.DateTimeField(null=False, auto_now=True)

class Feedback(models.Model):
    id = models.AutoField(primary_key=True)
    customer_id = models.ForeignKey(Customer, to_field='id', on_delete=models.CASCADE)
    employee_id = models.ForeignKey(Employee, to_field='id', on_delete=models.CASCADE)
    status = models.IntegerField(null=False)
    priority = models.IntegerField(null=False)
    sent_date = models.DateTimeField(null=False)
    header = models.TextField(null=False)
    content = models.TextField(null=False)
    date_create = models.DateTimeField(null=False, auto_now=True)