# Generated by Django 5.1.3 on 2024-11-15 12:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0012_customuser_employee_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attendancerecord',
            name='emp_no',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='employee_number',
        ),
    ]
