from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from .models import StudentProfile, Course, Enrollment


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'title']


class StudentProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)

    class Meta:
        model = StudentProfile
        fields = ['id', 'first_name', 'last_name', 'age', 'phone']


class EnrollmentReadSerializer(serializers.ModelSerializer):
    student = StudentProfileSerializer(read_only=True)
    course = CourseSerializer(read_only=True)

    class Meta:
        model = Enrollment
        fields = ['id', 'student', 'course', 'priority']


class EnrollmentWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = ['id', 'student', 'course', 'priority']
        validators = [
            UniqueTogetherValidator(
                queryset=Enrollment.objects.all(),
                fields=['student', 'course'],
                message="This student is already enrolled in this course."
            )
        ]
