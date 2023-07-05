from django.db import models
from user.models import User
from django.conf import settings


class Course(models.Model):
    title = models.CharField(max_length=303)
    image = models.FileField(upload_to='course/')
    price = models.CharField(max_length=202)
    duration = models.CharField(max_length=202)
    body = models.TextField()
    create_data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    @property
    def image_path(self):
        return f"{settings.SITE_URL}{self.image.url}"


class Lesson(models.Model):
    course = models.ForeignKey(Course, models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=404)

    def __str__(self):
        return self.title


class Task(models.Model):
    title = models.CharField(max_length=202)
    lesson = models.ForeignKey(Lesson, models.CASCADE, related_name='tasks')
    body = models.TextField()

    def __str__(self):
        return self.title


class ForExample(models.Model):
    task = models.ForeignKey(Task, models.CASCADE, related_name='for_examples')
    input = models.TextField()
    output = models.TextField()

    def __str__(self):
        return self.input


class UserAnswer(models.Model):
    STATUS = (
        ('Waiting', 'Waiting'),
        ('Wrong Answer', 'Wrong Answer'),
        ('Accepted', 'Accepted'),
    )
    user = models.ForeignKey(User, models.CASCADE, related_name='user_answers')
    task = models.ForeignKey(Task, models.CASCADE, related_name='user_answers')
    status = models.CharField(max_length=404, choices=STATUS, default='Waiting')
    code = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.name


class UserCourse(models.Model):
    user = models.ForeignKey(User, models.CASCADE, related_name='user_courses')
    course = models.ForeignKey(Course, models.CASCADE, related_name='user_courses')

    def __str__(self):
        return self.user.name
