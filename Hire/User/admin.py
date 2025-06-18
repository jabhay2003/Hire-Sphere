from django.contrib import admin
from .models import UserProfile
from .models import Contact
from .models import Company
from .models import JobPost
from .models import Application

# Register your models here.

admin.site.register(UserProfile)
admin.site.register(Contact)
admin.site.register(Company)
admin.site.register(JobPost)
admin.site.register(Application)