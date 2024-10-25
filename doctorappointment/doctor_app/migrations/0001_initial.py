# Generated by Django 5.1 on 2024-10-23 05:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=100)),
                ('phone_number', models.CharField(default='', max_length=15)),
                ('specialization', models.CharField(default='', max_length=150)),
                ('qualification', models.CharField(default='', max_length=150)),
                ('experience', models.CharField(default='', max_length=50)),
                ('email', models.CharField(max_length=100, unique=True)),
                ('password', models.CharField(default='', max_length=100)),
                ('utype', models.CharField(default='doctor', max_length=10)),
                ('status', models.CharField(default='pending', max_length=20)),
                ('image', models.ImageField(blank=True, null=True, upload_to='doctors')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=100)),
                ('phone_number', models.CharField(default='', max_length=15)),
                ('age', models.IntegerField()),
                ('email', models.CharField(max_length=100, unique=True)),
                ('password', models.CharField(default='', max_length=100)),
                ('utype', models.CharField(default='user', max_length=10)),
            ],
        ),
    ]
