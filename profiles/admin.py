from django.contrib import admin
from .models import Profile, LoginHistory, CustomUser, UserProfile, AttendanceRecord

# Register your models here.

admin.site.register(Profile)

admin.site.register(LoginHistory)
admin.site.register(CustomUser)
admin.site.register(UserProfile)
admin.site.register(AttendanceRecord)
