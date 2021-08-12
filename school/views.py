from django.views.generic import ListView
from django.shortcuts import render

from .models import Student, Teacher


def students_list(request):
    template = 'school/students_list.html'
    ordering = 'group'
    students = Student.objects.all().order_by(ordering).prefetch_related('teacher')
    context = {
        'object_list': students
    }
    return render(request, template, context)
