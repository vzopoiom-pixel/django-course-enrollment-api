from django.contrib import admin
from .models import Course, StudentProfile, Enrollment

admin.site.register(Course)
admin.site.register(StudentProfile)
admin.site.register(Enrollment)
