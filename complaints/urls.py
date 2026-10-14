from django.urls import path
from . import views

urlpatterns =[
    path('', views.landing, name='landing'),
    path('about-us/',views.about,name='about'),
    path('services/',views.services,name='services'),
    path('contact-us/',views.contact,name='contact'),
]