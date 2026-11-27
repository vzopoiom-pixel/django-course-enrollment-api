from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator


class Course(models.Model):
    title = models.CharField(max_length=100, verbose_name="Course Title")

    def __str__(self):
        return self.title


class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    age = models.PositiveIntegerField(
        validators=[MinValueValidator(12), MaxValueValidator(18)],
        verbose_name="Age"
    )
    phone_regex = RegexValidator(
        regex=r'^\+380\d{9}$',
        message="Phone number must be in the format: '+380XXXXXXXXX'."
    )
    phone = models.CharField(validators=[phone_regex], max_length=13, verbose_name="Phone")

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} ({self.user.username})"


class Enrollment(models.Model):
    PRIORITY_CHOICES = [
        (1, '1 (Highest)'),
        (2, '2 (Medium)'),
        (3, '3 (Lowest)'),
    ]
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Course")
    priority = models.IntegerField(choices=PRIORITY_CHOICES, verbose_name="Priority")

    class Meta:
        ordering = ['priority']
        constraints = [
            models.UniqueConstraint(
                fields=['student', 'course'],
                name='unique_student_course_enrollment'
            )
        ]
