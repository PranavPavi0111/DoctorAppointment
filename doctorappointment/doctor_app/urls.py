from django.contrib import admin
from .import views
from django.urls import path,include,re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from  rest_framework.routers import DefaultRouter
from .views import *

schema_view = get_schema_view(
    openapi.Info(
        title="Doctor App API",
        default_version="v1",
        description="API documentation for the Doctor App.",
        terms_of_service="https://www.google.com/policies/terms/",
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

router = DefaultRouter()
router.register(r"user_register",UserRegistrationView,basename='user_register')
router.register(r"doctor_register",DoctorRegistrationView,basename='doctor_register')
router.register(r"view_user_profile",ViewUserProfileView,basename='view_user_profile')
router.register(r"view_doctor_profile",ViewDoctorProfileView,basename='view_doctor_profile')
router.register(r"add_disease",AddDiseaseView,basename='add_disease')
router.register(r"search_disease",SearchDiseaseView,basename='search_disease')
router.register(r"book_appointment",BookAppointmentView,basename='book_appointment')
router.register(r"remove_disease",RemoveDiseaseView,basename='remove_disease')
router.register(r"admin_remove_doctor",AdminDeleteDoctorView,basename='admin_remove_doctor')
router.register(r"user_feedback",UserFeedbackView,basename='user_feedback')

urlpatterns = [
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(
        "redoc/",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
    
    path('',include(router.urls)),
    path('login/', LoginView.as_view(), name='login'),
    path('update_user_profile/',UpdateUserProfileView.as_view(),name='update_user_profile'),
    path('update_doctor_profile/',UpdateDoctorProfileView.as_view(),name='update_doctor_profile'),
    path('user_view_doctor/',UserViewDoctorView.as_view({'get':'list'}),name='user_view_doctor'),
    path('doctor_view_appointment/',DoctorViewAppointmentView.as_view({'get':'list'}),name='doctor_view_appointment'),
    path('user_view_appointment/',UserViewAppointmentView.as_view({'get':'list'}),name='user_view_appointment'),
    path('view_disease/',ViewDiseaseView.as_view({'get':'list'}),name='view_disease'),
    path('update_disease/',UpdateDiseaseView.as_view(),name='update_disease'),
    path('approve_doctor/',AdminApproveDoctorView.as_view(),name='approve_doctor'),
    path('admin_view_user/',AdminViewUserView.as_view({'get':'list'}),name='admin_view_user'),
    path('doctor_approve_booking/',DoctorApproveBookingView.as_view(),name='doctor_approve_booking'),
    path('send_message/', views.send_message, name='send_message'),
    path('get_chat_history/<int:user_id>/<int:doctor_id>/', views.get_chat_history, name='get_chat_history'),
    path('appointments/<int:appointment_id>/decline/', DeclineAppointmentView.as_view(), name='decline-appointment'),
    path('doctor_view_payment/',DoctorViewPaymentView.as_view({'get':'list'}),name='doctor_view_payment'),
    path('view_feedback/',AdminViewFeedback.as_view({'get':'list'}),name='view_feedback'),
]