from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.response import Response
from rest_framework import status,viewsets,generics
from rest_framework.views import APIView
from rest_framework.decorators import api_view

# Create your views here.


class UserRegistrationView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserRegisterSerializer
    http_method_names = ['post']
    def create(self,request,*args,**kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            response_data = {
                "status": "success",
                "message": "User created successfuly"
            }
            return Response(response_data,status=status.HTTP_200_OK)
        else:
            response_data = {
                "status": "failed",
                "message": "Invalid Details"
            }
            return Response(response_data,status=status.HTTP_400_BAD_REQUEST)


class DoctorRegistrationView(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    permission_classes = [AllowAny]
    serializer_class =  DoctorRegisterSerializer
    http_method_names = ['post']
    def create(self,request,*args,**kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            response_data = {
                "status": "success",
                "message": "User created successfuly"
            }
            return Response(response_data,status=status.HTTP_200_OK)
        else:
            response_data = {
                "status": "failed",
                "message": "Invalid Details"
            }
            return Response(response_data,status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')

            try:
                user = User.objects.get(email=email)
                if password == user.password: 
                    response_data = {
                        "status": "success",
                        "message": "User logged in successfully",
                        "utype": "user",
                        "user_id": user.id
                    }
                    request.session['id'] = user.id
                    return Response(response_data, status=status.HTTP_200_OK)
                else:
                    return Response({"status": "failed", "message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
            except User.DoesNotExist:
                pass

            
            try:
                doctor = Doctor.objects.get(email=email)
                if password == doctor.password:  
                    if  doctor.status == 'approved':
                        response_data = {
                            "status": "success",
                            "message": "Doctor logged in successfully",
                            "utype": "doctor",
                            "doctor_id": doctor.id,
                            "status": doctor.status
                        }
                        request.session['id'] = doctor.id
                        return Response(response_data, status=status.HTTP_200_OK)
                    else:
                       response_data={
                            "status": "Failed",
                            "message": "Doctor Must be approved by the admin",
                            } 
                    return Response(response_data, status=status.HTTP_200_OK)
                else:
                    return Response({"status": "failed", "message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
            except Doctor.DoesNotExist:
                pass

            try:
                admin = Admin.objects.get(email=email)
                if password == user.password: 
                    response_data = {
                        "status": "success",
                        "message": "Admin logged in successfully",
                    }
                    request.session['id'] = admin.id
                    return Response(response_data, status=status.HTTP_200_OK)
                else:
                    return Response({"status": "failed", "message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
            except User.DoesNotExist:
                pass
        else:
            return Response({"status": "failed", "message": "Invalid input"}, status=status.HTTP_400_BAD_REQUEST)
        

class ViewUserProfileView(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = ViewUserProfileSerializer

    def retrieve(self, request, *args, **kwargs):
        user = self.request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UpdateUserProfileView(generics.UpdateAPIView):
    serializer_class = UpdateUserProfileSerializer
    queryset = User.objects.all()

    def update(self, request, *args, **kwargs):
        # Retrieve user_id from session
        user_id = request.session.get('id')  # Ensure this matches the key you used to store the ID

        if user_id is None:
            return Response({"detail": "User ID not found in session."}, status=status.HTTP_403_FORBIDDEN)

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        # Proceed with profile update
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response({"detail": "Profile updated successfully."}, status=status.HTTP_200_OK)

class UpdateDoctorProfileView(generics.UpdateAPIView):
    serializer_class = UpdateDoctorProfileSerializer
    queryset = Doctor.objects.all()

    def update(self, request, *args, **kwargs):
        docotr_id = request.session.get('doctor_id')
        doctor = Doctor.objects.get(id=docotr_id)
        serializer = self.get_serializer(doctor,data=request.data,partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({"detail": "Profile updated successfully."}, status=status.HTTP_200_OK)
    
class ViewDoctorProfileView(viewsets.ReadOnlyModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = ViewDoctorProfileSerializer

    def retrieve(self, request, *args, **kwargs):
        doctor = self.request.user
        serializer = self.get_serializer(doctor)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class UserViewDoctorView(viewsets.ReadOnlyModelViewSet):
    queryset = Doctor.objects.filter(status='approved')
    serializer_class = UserViewDoctorSerializer

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    

class AdminApproveDoctorView(generics.UpdateAPIView):
    queryset = Doctor.objects.all()
    serializer_class = ApproveDoctorSerializer

    def update(self, request, *args, **kwargs):
        # doctor = self.get_object()
        admin_id = request.session.get('id')
        admin = Admin.objects.get(id=admin_id)
        if admin:
            doctor_id = request.data.get('id')
            doctor = Doctor.objects.get(id=doctor_id)
            serializer = self.get_serializer(doctor, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response({"detail": "Doctor approved"}, status=status.HTTP_200_OK)
        else:
            return Response({'detail':'invalid user'},status=status.HTTP_401_UNAUTHORIZED)



class AdminViewUserView(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer

    def  list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class AdminDeleteDoctorView(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()

    def destroy(self, request, *args, **kwargs):
        doctor_id = request.data.get('doctor_id')
        doctor = Doctor.objects.get(id=doctor_id)
        doctor.delete()
        return Response({"detail": "Doctor removed successfully."}, status=status.HTTP_200_OK)
    

class AddDiseaseView(viewsets.ModelViewSet):
    queryset = Disease.objects.all()
    serializer_class = DiseaseSerializer
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        id = request.session.get('id')
        admin = Admin.objects.get(id=id,utype='admin')
        if not admin:
            return Response({"detail": "You are not an admin"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
        return Response({"detail": "Disease added successfully."}, status=status.HTTP_201_CREATED)
    

class ViewDiseaseView(viewsets.ReadOnlyModelViewSet):
    queryset = Disease.objects.all()
    serializer_class = DiseaseSerializer

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    

class UpdateDiseaseView(generics.UpdateAPIView):
    queryset =  Disease.objects.all()
    serializer_class = DiseaseSerializer

    def update(self, request, *args, **kwargs):
        disease_id = request.data.get('id')
        disease = Disease.objects.get(id=disease_id)
        serializer = self.get_serializer(disease, data=request.data, partial=True)
        self.perform_update(serializer)
        return Response({"detail":"Disease updated successfully."}, status=status.HTTP_200_OK)



class RemoveDiseaseView(viewsets.ModelViewSet):
    queryset = Disease.objects.all()
    serializer_class = DiseaseSerializer

    def destroy(self, request, *args, **kwargs):
        disease_id = request.data.get('disease_id')
        disease = Disease.objects.filter(id=disease_id)
        disease.delete()
        return Response({"detail": "Disease removed successfully."}, status=status.HTTP_200_OK)
    
    

class SearchDiseaseView(viewsets.ModelViewSet):
    queryset = Disease.objects.all()
    serializer_class = SearchDiseaseSerializer

    def list(self,request):
        name = request.data.get('name')
        symptoms = request.data.get('symptoms')
        disease_type = request.data.get('type')

        if name:
            disease = Disease.objects.filter(name__icontains=name)
        elif symptoms:
            disease = Disease.objects.filter(symptoms__icontains=symptoms)
        elif disease_type:
            disease = Disease.objects.filter(type__icontains=disease_type)
        else:
            disease = Disease.objects.all()

        serializer = self.get_serializer(disease, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class BookAppointmentView(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = BookAppointmentSerializer
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        user_id = request.session.get('user')
        doctor_id = request.data.get('doctor')
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        try:
            doctor = Doctor.objects.get(id=doctor_id)
        except Doctor.DoesNotExist:
            return Response({"error": "Doctor not found"}, status=status.HTTP_404_NOT_FOUND)
        
        appointment_data = {
            'user': user.id,
            'doctor': doctor.id
        }

        serializer = self.get_serializer(data=appointment_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class DoctorViewAppointmentView(viewsets.ReadOnlyModelViewSet):
    queryset = Appointment.objects.filter(status='pending')
    serializer_class = DoctorViewAppointmentSerializer

    def list(self, request, *args, **kwargs):
        doctor = request.session.get('id')
        appointmnets = Appointment.objects.filter(doctor_id=doctor)
        return super().list(appointmnets, *args, **kwargs)
    

class UserViewAppointmentView(viewsets.ReadOnlyModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = UserViewAppointmentSerializer

    def list(self, request, *args, **kwargs):
        user = request.session.get('id')
        appointmnets = Appointment.objects.filter(user_id=user)
        return super().list(appointmnets, *args, **kwargs)
    

class DoctorApproveBookingView(generics.UpdateAPIView):
    queryset = Appointment.objects.all()
    serializer_class = DocApproveBookingSerializer

    def update(self, request, *args, **kwargs):
        appointment_id = request.data.get('id')
        appointment = Appointment.objects.get(id=appointment_id)
        serializer = self.get_serializer(appointment, data=request.data, partial=True)
        self.perform_update(serializer)


@api_view(['POST'])
def send_message(request):

    serializer = ChatMessageSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        return Response({"status": "success", "message": "Message sent successfully."}, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_chat_history(request, user_id, doctor_id):
    messages = ChatMessage.objects.filter(
        (models.Q(sender_user=user_id) & models.Q(receiver_doctor=doctor_id)) |
        (models.Q(sender_doctor=doctor_id) & models.Q(receiver_user=user_id))
    ).order_by('timestamp')
    
    serializer = ChatMessageSerializer(messages, many=True)
    return Response(serializer.data)


class DeclineAppointmentView(APIView):
    def post(self, request, appointment_id):
        doctor_id = request.session.get('id')  # Get doctor ID from the request data
        if not doctor_id:
            return Response({'error': 'Doctor ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Retrieve the doctor instance by ID
            doctor = Doctor.objects.get(id=doctor_id)

            # Retrieve the appointment for the specified doctor
            appointment = Appointment.objects.get(id=appointment_id, doctor=doctor)

        except Doctor.DoesNotExist:
            return Response({'error': 'Doctor not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Appointment.DoesNotExist:
            return Response({'error': 'Appointment not found or you are not authorized to decline it.'}, status=status.HTTP_404_NOT_FOUND)

        # Change the appointment status to 'declined'
        serializer = DeclineAppointmentSerializer(appointment, data={'status': 'declined'}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': 'Appointment declined and payment status updated.'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class DoctorViewPaymentView(viewsets.ReadOnlyModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def list(self, request, *args, **kwargs):
        doctor_id =  request.session.get('id')
        payment = Payment.objects.filter(doctor_id = doctor_id)
        return super().list(payment, *args, **kwargs)
    

class UserFeedbackView(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = UserFeedbackSerializer
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        user_id = request.session.get('id')
        
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            feedback_instance = Feedback(
                user_id=user_id,  
                feedback=serializer.validated_data['feedback']
            )
            feedback_instance.save()  # Save the instance to the database
            
            response_data = {
                "status": "success",
                "message": "feedback uploaded"
            }
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            response_data = {
                "status": "failed",
                "message": "invalid details"
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        
    
class AdminViewFeedback(viewsets.ReadOnlyModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = UserFeedbackSerializer

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)