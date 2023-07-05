from django.contrib import admin
from .models import UserCourse, Course, Lesson, ForExample, UserAnswer, Task
from .translations import CustomTranslationsAdmin, TranslationsInlineAdmin


@admin.register(UserCourse)
class Admin(admin.ModelAdmin):
    list_display = ['user', 'course']


@admin.register(UserAnswer)
class Admin(admin.ModelAdmin):
    list_display = ['user', 'status', 'created_date']
    list_filter = ['status']


class ForExampleInline(TranslationsInlineAdmin):
    model = ForExample
    extra = 0


@admin.register(Task)
class Admin(CustomTranslationsAdmin):
    inlines = [ForExampleInline]


class LessonInline(TranslationsInlineAdmin):
    model = Lesson
    extra = 0


@admin.register(Course)
class Admin(CustomTranslationsAdmin):
    inlines = [LessonInline]
