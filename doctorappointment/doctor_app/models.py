from datetime import timezone
from django.db import models

# Create your models here.


class User(models.Model):
    name = models.CharField(max_length=100,default='')
    phone_number = models.CharField(max_length=15,default='')
    age = models.IntegerField()
    email = models.CharField(max_length=100,unique=True)
    password = models.CharField(max_length=100,default='')
    utype = models.CharField(max_length=10,default='user')

class Doctor(models.Model):
    name = models.CharField(max_length=100,default='')
    phone_number = models.CharField(max_length=15,default='')
    specialization = models.CharField(max_length=150,default='')
    qualification = models.CharField(max_length=150,default='')
    experience = models.CharField(max_length=50,default='')
    email = models.CharField(max_length=100,unique=True)
    password = models.CharField(max_length=100,default='')
    utype = models.CharField(max_length=10,default='doctor')
    status = models.CharField(max_length=20,default='pending')
    image = models.ImageField(upload_to='doctors',null=True,blank=True)
    doctor_fee = models.IntegerField(null=True)

class Disease(models.Model):
    name = models.CharField(max_length=100,default='')
    symptoms = models.JSONField(default=list)
    type =  models.CharField(max_length=50,default='')

class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_appointments')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='doctor_appointments')
    name = models.CharField(max_length=100,default='')
    phone_number = models.CharField(max_length=15,default='')
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    status = models.CharField(max_length=20,default='pending')


class Admin(models.Model):
    username = models.CharField(max_length=100,default='')
    password = models.CharField(max_length=100,default='')
    email = models.CharField(max_length=100,unique=True)
    utype = models.CharField(max_length=20,default='admin')


class ChatMessage(models.Model):
    sender_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # User sending the message
    sender_doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True, blank=True)  # doctor sending the message
    receiver_user = models.ForeignKey(User, related_name='receiver_user', on_delete=models.CASCADE, null=True, blank=True)  # User receiving the message
    receiver_doctor = models.ForeignKey(Doctor, related_name='receiver_doctor', on_delete=models.CASCADE, null=True, blank=True)  # doctor receiving the message
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Message from {self.sender_user or self.sender_doctor} to {self.receiver_user or self.receiver_doctor} at {self.timestamp}'


class Payment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_payment',null=True,blank=True)
    doctor = models.ForeignKey(Doctor,on_delete=models.CASCADE,related_name='doctor_payment',null=True,blank=True)
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name='payment',null=True,blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    payment_status = models.CharField(max_length=20, default='pending')  


class Feedback(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    feedback = models.TextField()
    