from django.contrib import admin

# Register your models here.
from.models import CustomUser,PriestProfile
admin.site.register(CustomUser)
admin.site.register(PriestProfile)
