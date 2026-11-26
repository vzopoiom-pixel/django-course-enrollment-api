from rest_framework import viewsets
from .models import StudentProfile, Course, Enrollment
from .serializer import (
    StudentProfileSerializer,
    CourseSerializer,
    EnrollmentReadSerializer,
    EnrollmentWriteSerializer,
)


class StudentViewSet(viewsets.ModelViewSet):
    queryset = StudentProfile.objects.select_related('user').all()
    serializer_class = StudentProfileSerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.select_related('student__user', 'course').all()

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return EnrollmentReadSerializer
        return EnrollmentWriteSerializer
