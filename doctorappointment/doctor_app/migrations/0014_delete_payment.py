# Generated by Django 5.1 on 2024-10-25 08:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('doctor_app', '0013_payment_amount_payment_appointment_payment_doctor_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='payment',
        ),
    ]