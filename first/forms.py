from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import BaseFormSet, formset_factory
from django.core.exceptions import ValidationError
from .models import Course


class StudentRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, label="Имя")
    last_name = forms.CharField(max_length=30, required=True, label="Фамилия")
    email = forms.EmailField(required=True, label="Email")
    age = forms.IntegerField(min_value=12, max_value=18, required=True, label="Возраст (12–18)")
    phone = forms.RegexField(
        regex=r'^\+380\d{9}$',
        error_messages={'invalid': "Введите номер в формате +380XXXXXXXXX"},
        label="Телефон"
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'age', 'phone')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Пользователь с таким email уже зарегистрирован.")
        return email


class CourseChoiceForm(forms.Form):
    course = forms.ModelChoiceField(
        queryset=Course.objects.all(),
        required=False,
        label="Курс"
    )
    priority = forms.ChoiceField(
        choices=[(1, '1'), (2, '2'), (3, '3')],
        required=False,
        label="Приоритет"
    )


class BaseCourseFormSet(BaseFormSet):
    def clean(self):
        if any(self.errors):
            return

        courses = []
        priorities = []

        for form in self.forms:
            if not form.cleaned_data or form.cleaned_data.get('DELETE'):
                continue

            course = form.cleaned_data.get('course')
            priority = form.cleaned_data.get('priority')

            if not course:
                continue

            if course in courses:
                raise ValidationError("Курсы не могут повторяться.")
            courses.append(course)

            if priority in priorities:
                raise ValidationError("Приоритеты должны быть уникальными (1, 2, 3).")
            priorities.append(priority)

        if len(courses) == 0:
            raise ValidationError("Выберите хотя бы один курс.")


CourseFormSet = formset_factory(
    CourseChoiceForm,
    formset=BaseCourseFormSet,
    extra=3,
    max_num=3
)
