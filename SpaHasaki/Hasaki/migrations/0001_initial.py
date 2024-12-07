# Generated by Django 5.1.3 on 2024-12-07 15:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('account_id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=255)),
                ('password', models.CharField(max_length=255)),
                ('role', models.IntegerField(default=0)),
                ('is_delete', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('customer_id', models.AutoField(primary_key=True, serialize=False)),
                ('customer_name', models.CharField(max_length=255)),
                ('phone_number', models.CharField(max_length=10, null=True)),
                ('email', models.EmailField(max_length=255, null=True)),
                ('created_date', models.DateTimeField(auto_now=True)),
                ('is_delete', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('employee_id', models.AutoField(primary_key=True, serialize=False)),
                ('employee_name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=255, null=True)),
                ('phone_number', models.CharField(max_length=10)),
                ('created_date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('service_id', models.AutoField(primary_key=True, serialize=False)),
                ('service_name', models.CharField(max_length=255)),
                ('description', models.TextField(max_length=1024, null=True)),
                ('is_delete', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Messenger',
            fields=[
                ('messenger_id', models.AutoField(primary_key=True, serialize=False)),
                ('message_id', models.IntegerField()),
                ('message', models.TextField(null=True)),
                ('is_sent_from_customer', models.IntegerField()),
                ('sent_time', models.DateTimeField()),
                ('is_resolved', models.IntegerField()),
                ('is_delete', models.IntegerField(default=0)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Hasaki.customer')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Hasaki.employee')),
            ],
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('request_id', models.AutoField(primary_key=True, serialize=False)),
                ('employee_id', models.IntegerField(null=True)),
                ('status', models.IntegerField(default=0)),
                ('prioritize', models.IntegerField(default=2)),
                ('request_content', models.TextField()),
                ('request_date', models.DateTimeField()),
                ('is_delete', models.IntegerField(default=0)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Hasaki.customer')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Hasaki.service')),
            ],
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('appointment_id', models.AutoField(primary_key=True, serialize=False)),
                ('appointment_date', models.DateField()),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('status', models.IntegerField()),
                ('note', models.TextField(null=True)),
                ('is_delete', models.IntegerField(default=0)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Hasaki.customer')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Hasaki.employee')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Hasaki.service')),
            ],
        ),
        migrations.CreateModel(
            name='WorkShifts',
            fields=[
                ('shifts_id', models.AutoField(primary_key=True, serialize=False)),
                ('shifts_date', models.DateField()),
                ('shifts_detail', models.TextField()),
                ('is_delete', models.IntegerField(default=0)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Hasaki.employee')),
            ],
        ),
    ]
