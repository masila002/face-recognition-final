# Generated by Django 5.1.3 on 2024-11-15 08:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0011_attendancerecord_emp_no'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='employee_number',
            field=models.CharField(blank=True, max_length=20, null=True, unique=True),
        ),
    ]
