from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from rest_framework import viewsets

from .forms import StudentRegistrationForm, CourseFormSet
from .models import StudentProfile, Course, Enrollment
from .serializer import (
    StudentProfileSerializer,
    CourseSerializer,
    EnrollmentReadSerializer,
    EnrollmentWriteSerializer,
)


# --- Веб-интерфейс (HTML) ---

def register_view(request):
    if request.method == 'POST':
        user_form = StudentRegistrationForm(request.POST)
        formset = CourseFormSet(request.POST)

        if user_form.is_valid() and formset.is_valid():
            with transaction.atomic():
                user = user_form.save()
                profile = StudentProfile.objects.create(
                    user=user,
                    age=user_form.cleaned_data['age'],
                    phone=user_form.cleaned_data['phone']
                )
                for form in formset:
                    if form.cleaned_data and form.cleaned_data.get('course'):
                        Enrollment.objects.create(
                            student=profile,
                            course=form.cleaned_data['course'],
                            priority=form.cleaned_data['priority']
                        )
            login(request, user)
            return redirect('dashboard')
    else:
        user_form = StudentRegistrationForm()
        formset = CourseFormSet()

    return render(request, 'register.html', {
        'user_form': user_form,
        'formset': formset
    })


@login_required
def dashboard_view(request):
    if not hasattr(request.user, 'profile'):
        return redirect('/admin/')
    enrollments = request.user.profile.enrollments.select_related('course').all()
    return render(request, 'dashboard.html', {'enrollments': enrollments})


@login_required
def profile_view(request):
    if not hasattr(request.user, 'profile'):
        return redirect('/admin/')
    return render(request, 'profile.html', {'profile': request.user.profile})


# --- REST API (ViewSets) ---

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
