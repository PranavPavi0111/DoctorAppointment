# Generated by Django 5.1 on 2024-10-24 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctor_app', '0007_appointment_name_appointment_phone_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(default='', max_length=100)),
                ('password', models.CharField(default='', max_length=100)),
                ('email', models.CharField(max_length=100, unique=True)),
            ],
        ),
    ]