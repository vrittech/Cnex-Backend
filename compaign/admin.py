from django.contrib import admin
from .models import Faqs,Banner,PrivacyPolicy,HelpAndSupport,TermAndCondition

# Register your models here.
admin.site.register([Faqs,Banner,PrivacyPolicy,HelpAndSupport,TermAndCondition])
