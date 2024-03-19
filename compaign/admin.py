from django.contrib import admin
from .models import Faqs,Banner,PrivacyPolicy

# Register your models here.
admin.site.register([Faqs,Banner,PrivacyPolicy])
