# Generated by Django 5.1.3 on 2024-11-23 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SpaHasaki', '0002_rename_customer_id_appointment_customer_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='appointment_date',
            field=models.DateField(auto_now=True),
        ),
    ]