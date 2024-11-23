# Generated by Django 5.1.3 on 2024-11-23 08:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('SpaHasaki', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='appointment',
            old_name='customer_id',
            new_name='customer',
        ),
        migrations.RenameField(
            model_name='appointment',
            old_name='employee_id',
            new_name='employee',
        ),
        migrations.RenameField(
            model_name='appointment',
            old_name='service_id',
            new_name='service',
        ),
        migrations.RenameField(
            model_name='feedback',
            old_name='customer_id',
            new_name='customer',
        ),
        migrations.RenameField(
            model_name='feedback',
            old_name='employee_id',
            new_name='employee',
        ),
        migrations.RenameField(
            model_name='feedback',
            old_name='service_id',
            new_name='service',
        ),
        migrations.RenameField(
            model_name='workshifts',
            old_name='employee_id',
            new_name='employee',
        ),
    ]
