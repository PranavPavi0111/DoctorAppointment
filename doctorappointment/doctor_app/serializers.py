from .models import *
from rest_framework import serializers


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class DoctorRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = '__all__'

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=100)

class ViewUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'email', 'age', 'phone_number']

class UpdateUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields =  ['name','email', 'phone_number','age','password']


class ViewDoctorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields =  ['name','email', 'phone_number','experience','image','qualification','specialization']


class UpdateDoctorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields =  ['name','email', 'phone_number','experience','image','qualification','specialization','password','doctor_fee']


class UserViewDoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['name','email','phone_number','experience','image','specialization','qualification']


class DiseaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disease
        fields = '__all__'


class SearchDiseaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disease
        fields = '__all__'

class BookAppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'


class DoctorViewAppointmentSerializer(serializers.ModelSerializer):
    # patient_name = serializers.CharField(source='user.name',read_only=True)

    class Meta:
        model = Appointment
        fields = ['id', 'name', 'phone_number', 'date', 'time', 'status']


class UserViewAppointmentSerializer(serializers.ModelSerializer):
    doctor_name = serializers.CharField(source='doctor.name',read_only=True)

    class Meta:
        model = Appointment
        fields = ['id', 'doctor_name', 'name', 'phone_number', 'date', 'time', 'status']


class ApproveDoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = '__all__'

class DocApproveBookingSerializer(serializers.ModelSerializer):
    class Meta:    
        model = Appointment
        fields = ['status']


class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields ='__all__'

    def validate(self, data):
        sender_user = data.get('sender_user')
        sender_doctor = data.get('sender_doctor')
        receiver_user = data.get('receiver_user')
        receiver_doctor = data.get('receiver_doctor')

        # Ensure that either sender_user or sender_doctor is set
        if not sender_user and not sender_doctor:
            raise serializers.ValidationError("A sender (user or doctor) must be specified.")
        
        # Ensure that either receiver_user or receiver_doctor is set
        if not receiver_user and not receiver_doctor:
            raise serializers.ValidationError("A receiver (user or doctor) must be specified.")
        
        return data
    
class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class DeclineAppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['status']

    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)
        instance.save()

        # Update the related payment status
        payment = instance.payment
        if payment:
            payment.payment_status = 'refunded'
            payment.save()

        return instance
    

class UserFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'


class AdminRemoveDocSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['id']

class RemoveDiseaseSerializer(serializers.ModelSerializer):
    class Meta:
        model =  Disease
        fields = ['id']
