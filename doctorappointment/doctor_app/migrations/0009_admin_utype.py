# Generated by Django 5.1 on 2024-10-24 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctor_app', '0008_admin'),
    ]

    operations = [
        migrations.AddField(
            model_name='admin',
            name='utype',
            field=models.CharField(default='admin', max_length=20),
        ),
    ]
