from rest_framework import serializers
from .models import Course, Lesson, Task, ForExample


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['title', 'image_path', 'duration', 'price', 'body', 'lessons_count']

    lessons_count = serializers.SerializerMethodField()

    @staticmethod
    def get_lessons_count(obj):
        return obj.lessons.count()


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title']


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['title', 'tasks_count']

    tasks_count = serializers.SerializerMethodField()

    @staticmethod
    def get_tasks_count(obj):
        return obj.tasks.count()


class CourseDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['title', 'lessons_count']

    lessons_count = serializers.SerializerMethodField()

    @staticmethod
    def get_lessons_count(obj):
        return obj.lessons.count()


class ForExampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ForExample
        fields = ['input', 'output']


class TaskDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'body', 'for_examples']

    for_examples = ForExampleSerializer(many=True)
