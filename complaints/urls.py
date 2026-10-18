from django.urls import path
from . import views

urlpatterns =[
    path('', views.landing, name='landing'),
    path('about-us/',views.about,name='about'),
    path('services/',views.services,name='services'),
    path('contact-us/',views.contact,name='contact'),
    path('thankyou/', views.thankyou, name='thankyou'),
    path('student/register/', views.student_register, name='student_register'),
    path('student/login/', views.student_login, name='student_login'),
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('student/logout/', views.student_logout, name='student_logout'),
    path('student/complaint/new/', views.submit_complaint, name='submit_complaint'),
    path('student/track/', views.track_status, name='track_status'),
    path('student/complaint/<int:pk>/', views.complaint_detail, name='complaint_detail'),
    path('student/feedback/', views.give_feedback, name='give_feedback'),
    path('get-started/', views.choose_portal, name='choose_portal'),
]