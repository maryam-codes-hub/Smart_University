from django.contrib import admin

# Register your models here.
from .models import ContactMessage,Complaint

admin.site.register(ContactMessage)
admin.site.register(Complaint)