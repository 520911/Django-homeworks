from django.conf import settings
from django.core.exceptions import ValidationError
from rest_framework import serializers

from students.models import Course


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ("id", "name", "students")

    def validate_students(self, data):
        students = [stud.get('students') for stud in data]
        if len(students) > settings.MAX_STUDENTS_PER_COURSE:
            raise ValidationError(
                f'Максимальное число студентов на курсе: {settings.MAX_STUDENTS_PER_COURSE}')
        return data
