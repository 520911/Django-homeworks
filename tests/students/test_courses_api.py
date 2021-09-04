import pytest
from django.urls import reverse
from rest_framework import status

from students.models import Course
from students.serializers import CourseSerializer


def test_example():
    assert True


# проверка получения одного курса (retrieve-логика)
@pytest.mark.django_db
def test_check_one_course_detail(client, course_factory):
    courses = course_factory(_quantity=2)
    course = Course.objects.first()
    url = reverse('courses-detail', args=(course.id,))
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['name'] == course.name


# проверка получения списка курсов (list-логика)
@pytest.mark.django_db
def test_courses_list(client, course_factory):
    courses = course_factory(_quantity=2)
    url = reverse('courses-list')
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2


# тест успешного создания курса
@pytest.mark.django_db
def test_course_create(client):
    course = {'name': 'TestCourse'}
    url = reverse('courses-list')
    response = client.post(url, data=course)
    assert response.status_code == status.HTTP_201_CREATED


# тест успешного обновления курса
@pytest.mark.django_db
def test_course_update(client, course_factory):
    course = course_factory(name='TestCourse')
    update = {'name': 'BestCourse'}
    url = reverse('courses-detail', args=(course.id,))
    response = client.patch(url, data=update)
    assert response.status_code == status.HTTP_200_OK


# тест успешного удаления курса
@pytest.mark.django_db
def test_course_delete(client, course_factory):
    course = course_factory(name='TestCourse')
    url = reverse('courses-detail', args=(course.id,))
    response = client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT


# проверка фильтрации списка курсов по id
@pytest.mark.django_db
def test_filter_course_id(client, course_factory):
    courses = course_factory(_quantity=5)
    data = {'id': courses[0].id}
    url = reverse('courses-list')
    response = client.get(url, data=data)
    assert response.status_code == status.HTTP_200_OK


# проверка фильтрации списка курсов по name
@pytest.mark.django_db
def test_filter_course_name(client, course_factory):
    courses = course_factory(_quantity=5)
    data = {'name': courses[0].name}
    url = reverse('courses-list')
    response = client.get(url, data=data)
    assert response.status_code == status.HTTP_200_OK


# тест количества студентов на курсе
@pytest.mark.parametrize(
    ['students_count', 'status'],
    (
            (10, True),
            (15, True),
            (25, False)
    )
)
@pytest.mark.django_db
def test_count_student_in_course(students_count, status):
    students_list = [{'name': str(i)} for i in range(students_count)]
    serializer = CourseSerializer()
    course = {'name': 'TestCourse', 'students': students_list}
    if serializer.validate(course):
        result = True
        assert result == status
    else:
        result = False
        assert result == status
